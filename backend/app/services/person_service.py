"""
Person Service — business logic for person entities.
"""

from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.core.exceptions import NotFoundException, ConflictException
from app.database.repositories.person_repository import PersonRepository
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate

logger = get_logger(__name__)


class PersonService:
    """Service layer for Person operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = PersonRepository(session)

    async def create_person(self, person_data: PersonCreate) -> Person:
        """Create a new person after checking for conflicts."""
        # Check if person_id already exists
        existing = await self.repository.get_by_person_id(person_data.person_id)
        if existing:
            raise ConflictException(
                message=f"Person with ID {person_data.person_id} already exists",
                details={"person_id": person_data.person_id}
            )

        # Create the person
        person = Person(
            name=person_data.name,
            person_id=person_data.person_id,
            email=person_data.email,
            phone=person_data.phone,
            department=person_data.department,
            role=person_data.role,
            additional_info=person_data.additional_info,
            is_active=True
        )
        
        return await self.repository.create(person)

    async def get_person_by_id(self, person_uuid: UUID) -> Person:
        """Get person by internal UUID, raise if not found."""
        person = await self.repository.get_by_id(person_uuid)
        if not person:
            raise NotFoundException(message=f"Person {person_uuid} not found")
        return person

    async def get_person_by_person_id(self, person_id: str) -> Person:
        """Get person by external person_id, raise if not found."""
        person = await self.repository.get_by_person_id(person_id)
        if not person:
            raise NotFoundException(message=f"Person with ID {person_id} not found")
        return person

    async def update_person(self, person_uuid: UUID, updates: PersonUpdate) -> Person:
        """Update a person's information."""
        person = await self.get_person_by_id(person_uuid)
        
        # We only pass values that are set
        update_dict = updates.model_dump(exclude_unset=True)
        if not update_dict:
            return person
            
        return await self.repository.update(person, update_dict)

    async def delete_person(self, person_uuid: UUID) -> None:
        """Delete a person."""
        person = await self.get_person_by_id(person_uuid)
        await self.repository.delete(person)

    async def get_persons(
        self,
        page: int = 1,
        per_page: int = 50,
        search: Optional[str] = None,
        department: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Person], int]:
        """Get paginated persons list."""
        return await self.repository.get_all(
            page=page,
            per_page=per_page,
            search=search,
            department=department,
            is_active=is_active
        )
