"""
YOLO-based person detection and tracking.
"""

from typing import Any, Dict, List

import numpy as np
from ultralytics import YOLO

from app.core.logging_config import get_logger
from app.vision.base import BasePersonTracker

logger = get_logger(__name__)


class YoloPersonTracker(BasePersonTracker):
    """
    Person detection and tracking using Ultralytics YOLO and ByteTrack.
    """

    def __init__(self, model_name: str = "yolov8n.pt"):
        try:
            self.model = YOLO(model_name)
            logger.info("YOLO model loaded successfully", model=model_name)
        except Exception as e:
            logger.error("Failed to load YOLO model", error=str(e))
            raise

    def track(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect and track persons in the frame.
        
        Args:
            frame: BGR numpy array
            
        Returns:
            List of dictionaries containing tracking information.
        """
        # Run tracking, filter for class 0 (person), use bytetrack
        try:
            results = self.model.track(
                frame,
                classes=[0],
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False
            )
            
            tracked_persons = []
            
            if results and len(results) > 0:
                result = results[0]
                
                # Check if we have boxes and tracking IDs
                if result.boxes is not None and result.boxes.id is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    track_ids = result.boxes.id.cpu().numpy().astype(int)
                    confidences = result.boxes.conf.cpu().numpy()
                    
                    for box, track_id, conf in zip(boxes, track_ids, confidences):
                        x1, y1, x2, y2 = map(int, box)
                        tracked_persons.append({
                            "track_id": track_id,
                            "bbox": [x1, y1, x2, y2],
                            "confidence": float(conf)
                        })
            
            return tracked_persons
        except Exception as e:
            logger.error("Error during person tracking", error=str(e))
            return []
