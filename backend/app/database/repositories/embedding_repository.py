"""
Face embedding repository — data access for face vector storage.

Never exposes raw embeddings through API responses.
"""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

import numpy as np
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.models.face_embedding import FaceEmbedding

logger = get_logger(__name__)


class EmbeddingRepository:
    """Repository for face embedding CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        person_id: UUID,
        embedding: np.ndarray,
        model_name: str = "buffalo_l",
        quality_score: float = 0.0,
    ) -> FaceEmbedding:
        """Store a new face embedding for a person."""
        face_embedding = FaceEmbedding(
            person_id=person_id,
            embedding=embedding.tolist(),
            model_name=model_name,
            embedding_dimension=len(embedding),
            quality_score=quality_score,
        )
        self._session.add(face_embedding)
        await self._session.flush()
        await self._session.refresh(face_embedding)
        logger.info(
            "Face embedding stored",
            person_id=str(person_id),
            model=model_name,
            dimension=len(embedding),
        )
        return face_embedding

    async def get_by_person_id(self, person_id: UUID) -> List[FaceEmbedding]:
        """Get all face embeddings for a specific person."""
        result = await self._session.execute(
            select(FaceEmbedding).where(FaceEmbedding.person_id == person_id)
        )
        return list(result.scalars().all())

    async def delete_by_person_id(self, person_id: UUID) -> int:
        """Delete all face embeddings for a person. Returns count deleted."""
        result = await self._session.execute(
            delete(FaceEmbedding).where(FaceEmbedding.person_id == person_id)
        )
        await self._session.flush()
        count = result.rowcount
        logger.info("Face embeddings deleted", person_id=str(person_id), count=count)
        return count

    async def get_all_embeddings(self) -> List[FaceEmbedding]:
        """Get all stored face embeddings (for building recognition cache)."""
        result = await self._session.execute(select(FaceEmbedding))
        return list(result.scalars().all())

    async def exists_for_person(self, person_id: UUID) -> bool:
        """Check if any embedding exists for a person."""
        result = await self._session.execute(
            select(FaceEmbedding.id).where(
                FaceEmbedding.person_id == person_id
            ).limit(1)
        )
        return result.scalar_one_or_none() is not None
