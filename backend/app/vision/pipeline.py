"""
Vision Pipeline orchestrator.
"""

from typing import Any, Dict, List, Optional
import time

import numpy as np
import cv2

from app.core.logging_config import get_logger
from app.vision.person_tracker import YoloPersonTracker
from app.vision.face_detector import InsightFaceProvider
from app.vision.hand_detector import MediaPipeHandDetector
from app.vision.finger_counter import FingerCounter
from app.vision.eye_analyzer import EARAnalyzer
from app.vision.expression_analyzer import FERAnalyzer

logger = get_logger(__name__)


class VisionPipeline:
    """
    Orchestrates the entire vision pipeline, running sub-components at specific intervals
    to optimize performance.
    """

    def __init__(self, fps: int = 30):
        self.fps = fps
        self.frame_count = 0
        
        # Interval configuration (run every N frames)
        self.intervals = {
            "face_recognition": 5,
            "hand_detection": 2,
            "expression_analysis": 3,
        }
        
        # Initialize components
        try:
            self.tracker = YoloPersonTracker()
            self.face_provider = InsightFaceProvider()
            self.hand_detector = MediaPipeHandDetector()
            self.finger_counter = FingerCounter()
            self.eye_analyzer = EARAnalyzer(history_size=fps*2) # 2 seconds history
            self.expression_analyzer = FERAnalyzer()
            logger.info("Vision pipeline initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize vision pipeline", error=str(e))
            raise
            
        # State memory to persist data between intervals
        self.state_memory = {}

    def process_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Process a single frame through the pipeline.
        
        Args:
            frame: BGR numpy array
            
        Returns:
            List of detected events per person
        """
        self.frame_count += 1
        current_time = time.time()
        
        # Step 1: Detect and track persons (every frame)
        tracked_persons = self.tracker.track(frame)
        
        events = []
        current_track_ids = set()
        
        for person in tracked_persons:
            track_id = person["track_id"]
            bbox = person["bbox"]
            current_track_ids.add(track_id)
            
            x1, y1, x2, y2 = bbox
            
            # Ensure coordinates are within frame bounds
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            person_crop = frame[y1:y2, x1:x2]
            if person_crop.size == 0:
                continue
                
            # Initialize state memory for new track_id
            if track_id not in self.state_memory:
                self.state_memory[track_id] = {
                    "embedding": None,
                    "hands": [],
                    "fingers": 0,
                    "expression": "neutral",
                    "expression_confidence": 0.0,
                    "eye_state": "open",
                    "awake_status": "awake",
                    "face_bbox": None,
                    "face_confidence": 0.0
                }
                
            person_state = self.state_memory[track_id]
            
            # Step 2: Face Detection & Recognition
            faces = self.face_provider.detect(person_crop)
            if faces:
                # Assume largest face is the person's face
                face = faces[0]
                face_bbox = face["bbox"]
                
                # Convert face bbox relative to crop to absolute frame coordinates
                abs_face_bbox = [
                    face_bbox[0] + x1,
                    face_bbox[1] + y1,
                    face_bbox[2] + x1,
                    face_bbox[3] + y1
                ]
                person_state["face_bbox"] = abs_face_bbox
                person_state["face_confidence"] = face["confidence"]
                
                # Face Recognition (interval)
                if self.frame_count % self.intervals["face_recognition"] == 0:
                    person_state["embedding"] = face["embedding"]
                    
                # Eye Analysis (every frame for accurate temporal smoothing)
                if face["landmarks"] is not None:
                    # EAR analyzer requires landmarks
                    eye_results = self.eye_analyzer.analyze(face["landmarks"])
                    person_state["eye_state"] = eye_results["eye_state"]
                    person_state["awake_status"] = eye_results["awake_status"]
                    
                # Expression Analysis (interval)
                if self.frame_count % self.intervals["expression_analysis"] == 0:
                    # Extract face crop for FER
                    fx1, fy1, fx2, fy2 = map(int, face_bbox)
                    face_crop = person_crop[max(0, fy1):fy2, max(0, fx1):fx2]
                    if face_crop.size > 0:
                        expr_results = self.expression_analyzer.analyze(face_crop)
                        person_state["expression"] = expr_results["emotion"]
                        person_state["expression_confidence"] = expr_results["confidence"]
            else:
                person_state["face_bbox"] = None
                person_state["face_confidence"] = 0.0
                
            # Step 3: Hand & Finger Detection (interval)
            if self.frame_count % self.intervals["hand_detection"] == 0:
                hands = self.hand_detector.detect(person_crop)
                total_fingers = 0
                for hand in hands:
                    total_fingers += self.finger_counter.count(hand["landmarks"], hand["label"])
                person_state["hands"] = hands
                person_state["fingers"] = total_fingers
                
            # Compile event for this person
            events.append({
                "tracking_id": track_id,
                "bbox": bbox,
                "confidence": person["confidence"],
                "embedding": person_state["embedding"],  # Needs to be matched in service layer
                "face_bbox": person_state["face_bbox"],
                "face_confidence": person_state["face_confidence"],
                "hands_count": len(person_state["hands"]),
                "fingers_count": person_state["fingers"],
                "eye_state": person_state["eye_state"],
                "awake_status": person_state["awake_status"],
                "estimated_expression": person_state["expression"],
                "expression_confidence": person_state["expression_confidence"],
                "timestamp": current_time
            })
            
        # Clean up lost tracks
        lost_tracks = set(self.state_memory.keys()) - current_track_ids
        for track_id in lost_tracks:
            del self.state_memory[track_id]
            
        return events
