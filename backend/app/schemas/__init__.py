"""Pydantic request/response schemas."""

from app.schemas.person import (
    PersonCreate,
    PersonUpdate,
    PersonResponse,
    PersonListResponse,
    RegistrationResponse,
)
from app.schemas.detection import (
    DetectionPersonResult,
    DetectionFrameResult,
    DetectionControlRequest,
    DetectionStatusResponse,
)
from app.schemas.websocket import (
    WebSocketMessage,
    WebSocketDetectionMessage,
)

__all__ = [
    "PersonCreate",
    "PersonUpdate",
    "PersonResponse",
    "PersonListResponse",
    "RegistrationResponse",
    "DetectionPersonResult",
    "DetectionFrameResult",
    "DetectionControlRequest",
    "DetectionStatusResponse",
    "WebSocketMessage",
    "WebSocketDetectionMessage",
]
