"""
Registration Service — pipeline for validating images and registering faces.
"""

from typing import Any, Dict, Optional, Tuple
from uuid import UUID

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationException, NotFoundException
from app.core.logging_config import get_logger
from app.database.repositories.embedding_repository import EmbeddingRepository
from app.database.repositories.person_repository import PersonRepository
from app.vision.face_detector import InsightFaceProvider

logger = get_logger(__name__)


class RegistrationService:
    """Service layer for face registration pipeline."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.person_repo = PersonRepository(session)
        self.embedding_repo = EmbeddingRepository(session)
        # Face provider is instantiated here or injected
        self.face_provider = InsightFaceProvider()

    async def register_face(
        self, person_uuid: UUID, image_data: np.ndarray, replace_existing: bool = False
    ) -> Tuple[bool, str, Optional[float]]:
        """
        Process an image, extract face embedding, and store it for a person.
        
        Args:
            person_uuid: The UUID of the person to register
            image_data: BGR numpy array containing the face
            replace_existing: Whether to replace existing embeddings
            
        Returns:
            Tuple of (success boolean, message, quality score)
        """
        # Ensure person exists
        person = await self.person_repo.get_by_id(person_uuid)
        if not person:
            raise NotFoundException(message=f"Person {person_uuid} not found")

        # Check existing embeddings
        has_existing = await self.embedding_repo.exists_for_person(person_uuid)
        if has_existing and not replace_existing:
            raise ValidationException(message="Person already has a registered face")

        # Detect faces in the image
        faces = self.face_provider.detect(image_data)

        if not faces:
            raise ValidationException(message="No faces detected in the provided image")
            
        if len(faces) > 1:
            raise ValidationException(message="Multiple faces detected. Please provide an image with a single face")

        face = faces[0]
        
        # Validation rules
        confidence = face.get("confidence", 0.0)
        if confidence < 0.8:
            raise ValidationException(
                message=f"Face detection confidence too low: {confidence:.2f}. Please provide a clearer image."
            )

        embedding = face.get("embedding")
        if embedding is None:
            raise ValidationException(message="Failed to extract face embedding")

        # If replacing, delete old ones first
        if has_existing and replace_existing:
            await self.embedding_repo.delete_by_person_id(person_uuid)

        # Store new embedding
        await self.embedding_repo.create(
            person_id=person_uuid,
            embedding=embedding,
            model_name="buffalo_l",
            quality_score=confidence
        )

        return True, "Face successfully registered", confidence

    async def check_duplicate_face(self, image_data: np.ndarray) -> Optional[UUID]:
        """
        Check if the face in the image already belongs to someone else.
        Uses vector search.
        
        Args:
            image_data: BGR numpy array
            
        Returns:
            UUID of duplicate person if found, else None
        """
        from app.database.vector_search import VectorSearchService
        
        faces = self.face_provider.detect(image_data)
        if not faces:
            return None
            
        face = faces[0]
        embedding = face.get("embedding")
        if embedding is None:
            return None
            
        # Search DB for this embedding
        vector_service = VectorSearchService(self.session)
        matches = await vector_service.search(embedding, limit=1)
        
        if matches:
            match = matches[0]
            # Adjust threshold as needed based on model (cosine distance)
            if match["distance"] < 0.6:  # buffalo_l typically uses < 0.6 for same person
                return match["person_id"]
                
        return None
