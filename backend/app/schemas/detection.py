"""
Detection-related Pydantic schemas.

Defines the structure of detection results sent via WebSocket
and REST API responses for detection control.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DetectionPersonResult(BaseModel):
    """Detection result for a single person in a frame."""

    tracking_id: int
    person_id: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    bbox: List[int] = Field(default_factory=list, description="[x1, y1, x2, y2]")
    face_bbox: Optional[List[int]] = None
    face_confidence: float = 0.0
    hands_count: int = 0
    fingers_count: int = 0
    left_hand_fingers: Optional[int] = None
    right_hand_fingers: Optional[int] = None
    eye_state: str = "unknown"
    awake_status: str = "unknown"
    estimated_expression: str = "unknown"
    expression_confidence: float = 0.0
    is_known: bool = False
    match_score: float = 0.0


class DetectionFrameResult(BaseModel):
    """Complete detection result for a single frame."""

    frame_id: int
    timestamp: datetime
    fps: float = 0.0
    persons: List[DetectionPersonResult] = Field(default_factory=list)
    total_persons: int = 0
    recognized_persons: int = 0
    frame_base64: Optional[str] = Field(
        None, description="Base64-encoded annotated JPEG frame"
    )


class DetectionControlRequest(BaseModel):
    """Request to start/stop detection pipeline."""

    camera_source: Optional[str] = None
    detection_fps: Optional[int] = None


class DetectionStatusResponse(BaseModel):
    """Current detection pipeline status."""

    is_running: bool
    camera_connected: bool = False
    fps: float = 0.0
    total_detections: int = 0
    total_recognitions: int = 0
    uptime_seconds: float = 0.0
    active_tracks: int = 0


class PipelineMetrics(BaseModel):
    """Performance metrics for the detection pipeline."""

    detection_latency_ms: float = 0.0
    tracking_latency_ms: float = 0.0
    face_recognition_latency_ms: float = 0.0
    hand_detection_latency_ms: float = 0.0
    eye_analysis_latency_ms: float = 0.0
    expression_latency_ms: float = 0.0
    total_pipeline_latency_ms: float = 0.0
    fps: float = 0.0
    active_tracks: int = 0
    gpu_available: bool = False
