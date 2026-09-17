"""
Vector similarity search using pgvector.

Performs cosine similarity search against stored face embeddings
to identify registered persons from detected face embeddings.
"""

from __future__ import annotations

from typing import List, Optional, Tuple
from uuid import UUID

import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class VectorSearchResult:
    """Result of a vector similarity search."""

    def __init__(
        self,
        person_id: UUID,
        person_code: str,
        name: str,
        department: Optional[str],
        role: Optional[str],
        similarity: float,
    ):
        self.person_id = person_id
        self.person_code = person_code
        self.name = name
        self.department = department
        self.role = role
        self.similarity = similarity

    @property
    def is_match(self) -> bool:
        """Check if similarity exceeds the configured threshold."""
        return self.similarity >= settings.face_match_threshold

    def __repr__(self) -> str:
        return f"<VectorSearchResult(name='{self.name}', similarity={self.similarity:.3f})>"


class VectorSearch:
    """pgvector-based face embedding similarity search."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_similar(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        threshold: Optional[float] = None,
    ) -> List[VectorSearchResult]:
        """
        Search for the most similar face embeddings using cosine distance.

        pgvector's <=> operator computes cosine distance (1 - cosine_similarity).
        We convert to similarity: similarity = 1 - distance.

        Args:
            query_embedding: 512-dim face embedding to search for.
            top_k: Maximum number of results to return.
            threshold: Minimum similarity score. Defaults to config threshold.

        Returns:
            List of VectorSearchResult sorted by similarity (descending).
        """
        if threshold is None:
            threshold = settings.face_match_threshold

        embedding_str = "[" + ",".join(str(float(x)) for x in query_embedding) + "]"

        # Cosine distance via pgvector <=> operator
        # Lower distance = more similar; similarity = 1 - distance
        query = text("""
            SELECT
                p.id as person_id,
                p.person_id as person_code,
                p.name,
                p.department,
                p.role,
                1 - (fe.embedding <=> :embedding::vector) as similarity
            FROM face_embeddings fe
            JOIN persons p ON fe.person_id = p.id
            WHERE p.is_active = true
            ORDER BY fe.embedding <=> :embedding::vector
            LIMIT :top_k
        """)

        result = await self._session.execute(
            query,
            {"embedding": embedding_str, "top_k": top_k},
        )

        results = []
        for row in result.fetchall():
            vsr = VectorSearchResult(
                person_id=row.person_id,
                person_code=row.person_code,
                name=row.name,
                department=row.department,
                role=row.role,
                similarity=float(row.similarity),
            )
            results.append(vsr)

        if results:
            best = results[0]
            logger.debug(
                "Vector search completed",
                best_match=best.name,
                similarity=f"{best.similarity:.3f}",
                is_match=best.is_match,
            )

        return results

    async def find_best_match(
        self,
        query_embedding: np.ndarray,
        threshold: Optional[float] = None,
    ) -> Optional[VectorSearchResult]:
        """
        Find the single best matching person for a face embedding.

        Returns None if no match exceeds the threshold.
        """
        results = await self.find_similar(query_embedding, top_k=1, threshold=threshold)

        if results and results[0].is_match:
            return results[0]

        return None

    async def check_duplicate(
        self,
        query_embedding: np.ndarray,
        exclude_person_id: Optional[UUID] = None,
        duplicate_threshold: float = 0.85,
    ) -> Optional[VectorSearchResult]:
        """
        Check if a face embedding is a duplicate of an existing person.

        Uses a higher threshold than recognition to avoid false positives
        during registration.
        """
        results = await self.find_similar(
            query_embedding, top_k=1, threshold=duplicate_threshold
        )

        if not results:
            return None

        best = results[0]
        if best.similarity >= duplicate_threshold:
            if exclude_person_id and best.person_id == exclude_person_id:
                return None
            return best

        return None
