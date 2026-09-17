"""
Person SQLAlchemy model.

Represents a registered person in the system with their
profile information and associated face data.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Person(Base):
    """Registered person entity."""

    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    additional_info = Column(JSONB, default=dict)
    face_image_path = Column(String(500), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    face_embeddings = relationship(
        "FaceEmbedding",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    detection_events = relationship(
        "DetectionEvent",
        back_populates="person",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<Person(person_id='{self.person_id}', name='{self.name}')>"
