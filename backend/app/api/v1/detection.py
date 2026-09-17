"""
Detection endpoints (start/stop camera).
"""

from fastapi import APIRouter, HTTPException

from app.services.detection_service import detection_service

router = APIRouter()


@router.post("/start")
async def start_detection(camera_index: int = 0):
    """Start the computer vision detection service."""
    success = detection_service.start(camera_index)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start detection service")
    return {"status": "started", "message": "Detection service is running"}


@router.post("/stop")
async def stop_detection():
    """Stop the computer vision detection service."""
    detection_service.stop()
    return {"status": "stopped", "message": "Detection service has been stopped"}


@router.get("/status")
async def detection_status():
    """Get the current status of the detection service."""
    return {"is_running": detection_service.is_running}
