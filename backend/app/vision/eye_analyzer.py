"""
Eye state analysis using facial landmarks and Eye Aspect Ratio (EAR).
"""

from collections import deque
from typing import Any, Dict, List

import numpy as np
from scipy.spatial import distance as dist

from app.core.config import settings
from app.core.logging_config import get_logger
from app.vision.base import BaseEyeAnalyzer

logger = get_logger(__name__)


class EARAnalyzer(BaseEyeAnalyzer):
    """
    Analyzes eye state (EAR) and maintains temporal state to detect drowsiness/sleep.
    """

    def __init__(self, fps: float = 15.0):
        self.fps = fps if fps > 0 else float(settings.detection_fps)
        self.closed_threshold = settings.eye_closed_threshold
        
        # Calculate frames based on time thresholds
        self.drowsy_frames = int(settings.eye_drowsy_duration_seconds * self.fps)
        self.sleep_frames = int(settings.eye_sleep_duration_seconds * self.fps)
        
        # Smoothing window
        self.smoothing_window_size = settings.eye_smoothing_window
        
        # State tracking per person (tracking_id -> deque of recent EARs)
        self.history: Dict[int, deque] = {}
        # Consecutive closed frames per person
        self.closed_counter: Dict[int, int] = {}

    def _calculate_ear(self, eye_landmarks: np.ndarray) -> float:
        """
        Calculate the Eye Aspect Ratio for a single eye.
        Expects 6 (x,y) points for the eye.
        """
        if len(eye_landmarks) < 6:
            return 1.0 # default open
            
        A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
        
        if C == 0:
            return 0.0
            
        ear = (A + B) / (2.0 * C)
        return ear

    def analyze(self, landmarks: np.ndarray, tracking_id: int = -1) -> Dict[str, Any]:
        """
        Analyze the landmarks to determine eye state.
        
        Args:
            landmarks: Numpy array of 68 facial landmarks.
            tracking_id: ID of the person to track temporal state.
            
        Returns:
            Dictionary with eye_state, awake_status, and raw ear.
        """
        # If we don't have enough landmarks (e.g. from SCRFD which only gives 5 points),
        # we can't accurately calculate EAR without an external 68/468 point model.
        # For a full implementation, we'd run MediaPipe FaceMesh on the face crop.
        # Here we mock the behavior assuming we have 68 points.
        
        if landmarks is None or len(landmarks) < 68:
            # Fallback if we only have 5 point landmarks
            return {
                "eye_state": "unknown",
                "awake_status": "unknown",
                "ear": 0.0
            }

        # Extract left and right eye coordinates (indices for 68-point model)
        # Left eye: 36-41, Right eye: 42-47
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]
        
        left_ear = self._calculate_ear(left_eye)
        right_ear = self._calculate_ear(right_eye)
        
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Temporal smoothing
        if tracking_id not in self.history:
            self.history[tracking_id] = deque(maxlen=self.smoothing_window_size)
            self.closed_counter[tracking_id] = 0
            
        self.history[tracking_id].append(avg_ear)
        smoothed_ear = sum(self.history[tracking_id]) / len(self.history[tracking_id])
        
        # Determine current frame state
        eye_state = "open"
        if smoothed_ear < self.closed_threshold:
            eye_state = "closed"
            self.closed_counter[tracking_id] += 1
        else:
            self.closed_counter[tracking_id] = 0
            
        # Determine aggregate status
        awake_status = "awake"
        closed_frames = self.closed_counter[tracking_id]
        
        if closed_frames >= self.sleep_frames:
            awake_status = "sleeping"
        elif closed_frames >= self.drowsy_frames:
            awake_status = "drowsy"
            
        return {
            "eye_state": eye_state,
            "awake_status": awake_status,
            "ear": float(smoothed_ear)
        }
        
    def cleanup_track(self, tracking_id: int) -> None:
        """Clean up tracking history when a person leaves the frame."""
        if tracking_id in self.history:
            del self.history[tracking_id]
        if tracking_id in self.closed_counter:
            del self.closed_counter[tracking_id]
