"""
Hand and landmark detection using MediaPipe.
"""

from typing import Any, Dict, List

import cv2
import mediapipe as mp
import numpy as np

from app.core.logging_config import get_logger
from app.vision.base import BaseHandDetector

logger = get_logger(__name__)


class MediaPipeHandDetector(BaseHandDetector):
    """
    MediaPipe Hands based hand and landmark detector.
    """

    def __init__(self, max_hands: int = 2, min_detection_confidence: float = 0.5, min_tracking_confidence: float = 0.5):
        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=max_hands,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
            logger.info("MediaPipe Hand Detector initialized")
        except Exception as e:
            logger.error("Failed to initialize MediaPipe Hands", error=str(e))
            raise

    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect hands and landmarks in a frame (typically a person crop).
        
        Args:
            frame: BGR numpy array
            
        Returns:
            List of dictionaries, one for each detected hand, containing landmarks and handedness.
        """
        try:
            # MediaPipe requires RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            detected_hands = []
            
            if results.multi_hand_landmarks and results.multi_handedness:
                h, w, _ = frame.shape
                
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Convert normalized landmarks to pixel coordinates
                    landmarks_px = []
                    for lm in hand_landmarks.landmark:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        landmarks_px.append((cx, cy))
                        
                    label = handedness.classification[0].label # 'Left' or 'Right'
                    score = handedness.classification[0].score
                    
                    detected_hands.append({
                        "label": label,
                        "confidence": float(score),
                        "landmarks": landmarks_px,
                        "normalized_landmarks": [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                    })
                    
            return detected_hands
        except Exception as e:
            logger.error("Error during hand detection", error=str(e))
            return []
