"""
Recognition Service — matching detected face embeddings against the database.
"""

from typing import Dict, Optional, Tuple
from uuid import UUID

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.database.vector_search import VectorSearchService

logger = get_logger(__name__)


class RecognitionService:
    """Service layer for face recognition operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.vector_search = VectorSearchService(session)
        # Threshold for cosine distance (lower is more similar)
        # InsightFace buffalo_l standard is ~0.5-0.6 depending on desired precision/recall
        self.similarity_threshold = 0.55

    async def identify_face(self, embedding: np.ndarray) -> Tuple[Optional[UUID], float]:
        """
        Identify a person from a face embedding.
        
        Args:
            embedding: 512-dimensional vector from ArcFace
            
        Returns:
            Tuple of (person_uuid or None if unknown, distance score)
        """
        matches = await self.vector_search.search(embedding, limit=1)
        
        if not matches:
            return None, 1.0
            
        match = matches[0]
        distance = match["distance"]
        
        if distance <= self.similarity_threshold:
            return match["person_id"], distance
            
        return None, distance
