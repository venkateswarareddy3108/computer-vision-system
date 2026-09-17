"""
Facial expression recognition using FER library.
"""

from typing import Any, Dict

import numpy as np
from fer import FER

from app.core.config import settings
from app.core.logging_config import get_logger
from app.vision.base import BaseExpressionAnalyzer

logger = get_logger(__name__)


class FERExpressionAnalyzer(BaseExpressionAnalyzer):
    """
    Facial Expression Recognition using the FER library (MTCNN).
    """

    def __init__(self):
        try:
            # Initialize with MTCNN for better face detection internally
            self.detector = FER(mtcnn=True)
            self.threshold = settings.expression_confidence_threshold
            logger.info("FER Expression Analyzer initialized")
        except Exception as e:
            logger.error("Failed to initialize FER library", error=str(e))
            raise

    def analyze(self, face_image: np.ndarray) -> Dict[str, Any]:
        """
        Estimate facial expression from a face crop.
        
        Args:
            face_image: BGR numpy array of the face crop
            
        Returns:
            Dict containing estimated expression and confidence.
        """
        try:
            # FER can take the full image or a crop. We pass the crop.
            emotions = self.detector.detect_emotions(face_image)
            
            if emotions and len(emotions) > 0:
                # Get the dominant emotion and its score from the first detected face
                emotion_dict = emotions[0]["emotions"]
                dominant_emotion = max(emotion_dict, key=emotion_dict.get)
                score = emotion_dict[dominant_emotion]
                
                if score >= self.threshold:
                    return {
                        "estimated_expression": dominant_emotion,
                        "confidence": float(score)
                    }
                    
            return {
                "estimated_expression": "unknown",
                "confidence": 0.0
            }
        except Exception as e:
            logger.error("Error during expression analysis", error=str(e))
            return {
                "estimated_expression": "unknown",
                "confidence": 0.0
            }
