"""
DetectionEvent SQLAlchemy model.

Stores periodic snapshots of detection pipeline results.
Events are batch-inserted at configurable intervals to
prevent excessive database writes.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class DetectionEvent(Base):
    """Detection event snapshot entity."""

    __tablename__ = "detection_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_id = Column(Integer, nullable=False, index=True)
    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("persons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    hands_count = Column(Integer, default=0)
    fingers_count = Column(Integer, default=0)
    eye_state = Column(String(50), default="unknown")
    awake_status = Column(String(50), default="unknown")
    estimated_expression = Column(String(50), default="unknown")
    expression_confidence = Column(Float, default=0.0)
    face_confidence = Column(Float, default=0.0)
    bbox = Column(JSONB, nullable=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # Relationships
    person = relationship("Person", back_populates="detection_events")

    def __repr__(self) -> str:
        return f"<DetectionEvent(tracking_id={self.tracking_id}, person_id='{self.person_id}')>"
