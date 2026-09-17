"""
YOLO-based person detector.
"""

from typing import Any, Dict, List

import numpy as np
from ultralytics import YOLO

from app.core.logging_config import get_logger
from app.vision.base import BasePersonDetector

logger = get_logger(__name__)


class YoloPersonDetector(BasePersonDetector):
    """
    Person detection using Ultralytics YOLO.
    """

    def __init__(self, model_name: str = "yolov8n.pt"):
        try:
            self.model = YOLO(model_name)
            logger.info("YOLO model loaded successfully", model=model_name)
        except Exception as e:
            logger.error("Failed to load YOLO model", error=str(e))
            raise

    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect persons in the frame.
        
        Args:
            frame: BGR numpy array
            
        Returns:
            List of dictionaries containing detection information.
        """
        try:
            results = self.model(
                frame,
                classes=[0],
                verbose=False
            )
            
            detected_persons = []
            
            if results and len(results) > 0:
                result = results[0]
                
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    
                    for box, conf in zip(boxes, confidences):
                        x1, y1, x2, y2 = map(int, box)
                        detected_persons.append({
                            "bbox": [x1, y1, x2, y2],
                            "confidence": float(conf)
                        })
            
            return detected_persons
        except Exception as e:
            logger.error("Error during person detection", error=str(e))
            return []
