"""
WebSocket endpoints for real-time streaming.
"""

import asyncio
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.logging_config import get_logger
from app.services.detection_service import detection_service

logger = get_logger(__name__)
router = APIRouter()


@router.websocket("/ws/detection")
async def detection_websocket(websocket: WebSocket):
    """WebSocket endpoint for receiving real-time detection events."""
    await websocket.accept()
    
    # Create an asyncio queue for this connection
    queue = asyncio.Queue(maxsize=10)
    await detection_service.add_subscriber(queue)
    
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # Check if client is still connected by trying to receive
            # We use a timeout so we can mostly focus on sending
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                pass
                
            # Get data from detection service
            try:
                # Use a small timeout so we can still check for pings/disconnects
                msg = await asyncio.wait_for(queue.get(), timeout=1.0)
                await websocket.send_json(msg)
            except asyncio.TimeoutError:
                continue
                
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
    finally:
        await detection_service.remove_subscriber(queue)
