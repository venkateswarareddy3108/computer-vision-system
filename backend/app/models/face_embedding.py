"""
FaceEmbedding SQLAlchemy model.

Stores 512-dimensional ArcFace face embeddings using pgvector.
Linked to a registered person via foreign key.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class FaceEmbedding(Base):
    """Face embedding vector entity stored via pgvector."""

    __tablename__ = "face_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    embedding = Column(Vector(512), nullable=False)
    model_name = Column(String(100), nullable=False, default="buffalo_l")
    embedding_dimension = Column(Integer, nullable=False, default=512)
    quality_score = Column(Float, default=0.0)
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

    # Relationships
    person = relationship("Person", back_populates="face_embeddings")

    def __repr__(self) -> str:
        return f"<FaceEmbedding(person_id='{self.person_id}', model='{self.model_name}')>"
