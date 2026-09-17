"""
Face detection and recognition using InsightFace.
"""

from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

from app.core.config import settings
from app.core.logging_config import get_logger
from app.vision.base import BaseFaceDetector, BaseFaceRecognizer

logger = get_logger(__name__)


class InsightFaceProvider(BaseFaceDetector, BaseFaceRecognizer):
    """
    Combined Face Detector and Recognizer using InsightFace.
    Provides SCRFD for detection and ArcFace for embeddings.
    """

    def __init__(self):
        try:
            # Initialize the FaceAnalysis app
            # Automatically tries to use GPU if onnxruntime-gpu is installed
            self.app = FaceAnalysis(
                name=settings.face_model_name,
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
            )
            # Default detect size. Can be adjusted based on requirements.
            self.app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("InsightFace initialized", model=settings.face_model_name)
        except Exception as e:
            logger.error("Failed to initialize InsightFace", error=str(e))
            raise

    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect faces in a frame.
        """
        try:
            faces = self.app.get(frame)
            results = []
            
            for face in faces:
                x1, y1, x2, y2 = map(int, face.bbox)
                results.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": float(face.det_score),
                    "landmarks": face.kps,  # 5-point facial landmarks
                    "embedding": face.embedding, # 512-dim ArcFace embedding
                    # Depending on the model pack, age, gender, and emotion might be available
                    "age": getattr(face, 'age', None),
                    "gender": getattr(face, 'gender', None), 
                })
            return results
        except Exception as e:
            logger.error("Error during face detection", error=str(e))
            return []

    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Get the face embedding for a pre-cropped face image.
        Typically, InsightFace works best on the full image, but we can process crops.
        """
        faces = self.detect(face_image)
        if faces and len(faces) > 0:
            # Return the embedding of the most prominent face
            return faces[0]["embedding"]
        return None
