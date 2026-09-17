"""
WebSocket message schemas.

Defines the message format for real-time communication
between backend and frontend.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.detection import DetectionPersonResult, PipelineMetrics


class WebSocketMessage(BaseModel):
    """Generic WebSocket message envelope."""

    type: str = "detection"
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    data: Dict[str, Any] = Field(default_factory=dict)


class WebSocketDetectionMessage(BaseModel):
    """WebSocket message containing detection frame results."""

    type: str = "detection_frame"
    frame_id: int
    timestamp: datetime
    fps: float = 0.0
    persons: List[DetectionPersonResult] = Field(default_factory=list)
    total_persons: int = 0
    recognized_persons: int = 0
    metrics: Optional[PipelineMetrics] = None
    frame_base64: Optional[str] = None


class WebSocketStatusMessage(BaseModel):
    """WebSocket message for system status updates."""

    type: str = "status"
    is_running: bool
    camera_connected: bool = False
    message: str = ""


class WebSocketErrorMessage(BaseModel):
    """WebSocket message for error notifications."""

    type: str = "error"
    message: str
    recoverable: bool = True
