"""
Detection Service — orchestrates the camera, vision pipeline, and websocket broadcasting.
"""

import asyncio
import base64
from typing import Dict, Any, Optional

import cv2
import numpy as np

from app.core.logging_config import get_logger
from app.vision.pipeline import VisionPipeline
from app.services.recognition_service import RecognitionService
from app.database.connection import get_session
from app.database.repositories.person_repository import PersonRepository
from app.schemas.websocket import DetectionMessage

logger = get_logger(__name__)


class DetectionService:
    """Service for running the detection loop and broadcasting results."""

    def __init__(self):
        self.camera = None
        self.pipeline = None
        self.is_running = False
        self.task = None
        self.subscribers = set()
        self.person_cache = {}  # uuid -> person details (to avoid hitting DB for every frame)

    def start(self, camera_index: int = 0) -> bool:
        """Start the detection loop."""
        if self.is_running:
            return True
            
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                logger.error("Failed to open camera", index=camera_index)
                return False
                
            self.pipeline = VisionPipeline()
            self.is_running = True
            
            # Start background task
            self.task = asyncio.create_task(self._detection_loop())
            logger.info("Detection service started")
            return True
        except Exception as e:
            logger.error("Error starting detection service", error=str(e))
            self.stop()
            return False

    def stop(self):
        """Stop the detection loop."""
        self.is_running = False
        if self.task:
            self.task.cancel()
            self.task = None
            
        if self.camera:
            self.camera.release()
            self.camera = None
            
        self.pipeline = None
        logger.info("Detection service stopped")

    async def add_subscriber(self, queue: asyncio.Queue):
        """Add a queue to broadcast messages to."""
        self.subscribers.add(queue)
        
    async def remove_subscriber(self, queue: asyncio.Queue):
        """Remove a broadcast queue."""
        self.subscribers.discard(queue)

    async def _detection_loop(self):
        """Main loop that grabs frames, processes them, and broadcasts."""
        # Setup session for DB queries within loop
        # We need a context manager since this is a background task
        try:
            async for session in get_session():
                recognition_service = RecognitionService(session)
                person_repo = PersonRepository(session)
                
                while self.is_running:
                    start_time = asyncio.get_event_loop().time()
                    
                    ret, frame = self.camera.read()
                    if not ret:
                        logger.warning("Failed to grab frame")
                        await asyncio.sleep(0.1)
                        continue
                        
                    # Process frame
                    events = self.pipeline.process_frame(frame)
                    
                    # Resolve identities
                    for event in events:
                        embedding = event.pop("embedding", None)
                        
                        if embedding is not None:
                            # Search identity
                            person_uuid, distance = await recognition_service.identify_face(embedding)
                            
                            if person_uuid:
                                # Populate cache if missing
                                if person_uuid not in self.person_cache:
                                    person = await person_repo.get_by_id(person_uuid)
                                    if person:
                                        self.person_cache[person_uuid] = {
                                            "person_id": person.person_id,
                                            "name": person.name,
                                            "department": person.department
                                        }
                                
                                if person_uuid in self.person_cache:
                                    event["person"] = self.person_cache[person_uuid]
                                    event["person"]["uuid"] = str(person_uuid)
                                    event["distance"] = distance
                                    
                    # Draw boxes on frame for visualization (simple annotated frame)
                    annotated_frame = self._annotate_frame(frame, events)
                    
                    # Convert frame to JPEG base64
                    _, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                    frame_b64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # Create message
                    message = DetectionMessage(
                        frame=frame_b64,
                        events=events
                    )
                    
                    # Broadcast
                    if self.subscribers:
                        msg_dict = message.model_dump()
                        dead_queues = set()
                        for queue in self.subscribers:
                            try:
                                # Non-blocking put
                                queue.put_nowait(msg_dict)
                            except asyncio.QueueFull:
                                pass
                            except Exception:
                                dead_queues.add(queue)
                                
                        for q in dead_queues:
                            self.subscribers.discard(q)
                            
                    # Throttle to maintain consistent FPS (e.g., 30 fps)
                    elapsed = asyncio.get_event_loop().time() - start_time
                    delay = max(0, (1.0 / 30.0) - elapsed)
                    await asyncio.sleep(delay)
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Error in detection loop", error=str(e))
        finally:
            self.stop()

    def _annotate_frame(self, frame: np.ndarray, events: list) -> np.ndarray:
        """Draw bounding boxes and basic info on the frame."""
        annotated = frame.copy()
        
        for event in events:
            # Person bbox
            x1, y1, x2, y2 = map(int, event["bbox"])
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Label
            label = f"Track: {event['tracking_id']}"
            if "person" in event:
                label += f" | {event['person']['name']}"
                
            cv2.putText(annotated, label, (x1, max(0, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
            # Face bbox
            face_bbox = event.get("face_bbox")
            if face_bbox:
                fx1, fy1, fx2, fy2 = map(int, face_bbox)
                cv2.rectangle(annotated, (fx1, fy1), (fx2, fy2), (255, 0, 0), 2)
                
        return annotated

# Global singleton instance
detection_service = DetectionService()
