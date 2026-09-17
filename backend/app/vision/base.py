"""
Abstract base classes for the Computer Vision pipeline.

Defines the interfaces for different vision models to ensure
they can be easily swapped or mocked in tests.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class BasePersonDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect persons in a frame. Returns list of dicts with bbox and confidence."""
        pass


class BasePersonTracker(ABC):
    @abstractmethod
    def track(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Track persons across frames. Returns list of dicts with track_id and bbox."""
        pass


class BaseFaceDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect faces. Returns list with bbox, confidence, and landmarks."""
        pass


class BaseFaceRecognizer(ABC):
    @abstractmethod
    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """Generate a feature embedding for a cropped face image."""
        pass


class BaseHandDetector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect hands and landmarks in a frame."""
        pass


class BaseEyeAnalyzer(ABC):
    @abstractmethod
    def analyze(self, landmarks: np.ndarray) -> Dict[str, Any]:
        """Analyze eye state (open/closed, drowsiness) from landmarks."""
        pass


class BaseExpressionAnalyzer(ABC):
    @abstractmethod
    def analyze(self, face_image: np.ndarray) -> Dict[str, Any]:
        """Estimate facial expression from a face crop."""
        pass
