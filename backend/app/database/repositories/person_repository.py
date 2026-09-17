"""
Person repository — data access layer for Person entities.

All database queries are parameterized via SQLAlchemy ORM
to prevent SQL injection.
"""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.models.person import Person

logger = get_logger(__name__)


class PersonRepository:
    """Repository for Person CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, person: Person) -> Person:
        """Insert a new person record."""
        self._session.add(person)
        await self._session.flush()
        await self._session.refresh(person)
        logger.info("Person created", person_id=person.person_id, name=person.name)
        return person

    async def get_by_id(self, id: UUID) -> Optional[Person]:
        """Get a person by internal UUID."""
        result = await self._session.execute(
            select(Person).where(Person.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_person_id(self, person_id: str) -> Optional[Person]:
        """Get a person by their human-readable person_id (e.g. EMP001)."""
        result = await self._session.execute(
            select(Person).where(Person.person_id == person_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 50,
        search: Optional[str] = None,
        department: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[List[Person], int]:
        """
        Get paginated list of persons with optional filtering.

        Returns:
            Tuple of (persons list, total count).
        """
        query = select(Person)
        count_query = select(func.count(Person.id))

        # Apply filters
        if search:
            search_filter = or_(
                Person.name.ilike(f"%{search}%"),
                Person.person_id.ilike(f"%{search}%"),
                Person.email.ilike(f"%{search}%"),
                Person.department.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        if department:
            query = query.where(Person.department == department)
            count_query = count_query.where(Person.department == department)

        if is_active is not None:
            query = query.where(Person.is_active == is_active)
            count_query = count_query.where(Person.is_active == is_active)

        # Get total count
        total_result = await self._session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (page - 1) * per_page
        query = query.order_by(Person.created_at.desc()).offset(offset).limit(per_page)

        result = await self._session.execute(query)
        persons = list(result.scalars().all())

        return persons, total

    async def update(self, person: Person, updates: dict) -> Person:
        """Update a person's fields."""
        for key, value in updates.items():
            if value is not None and hasattr(person, key):
                setattr(person, key, value)
        await self._session.flush()
        await self._session.refresh(person)
        logger.info("Person updated", person_id=person.person_id)
        return person

    async def delete(self, person: Person) -> None:
        """Delete a person and cascade to face embeddings."""
        logger.info("Person deleted", person_id=person.person_id)
        await self._session.delete(person)
        await self._session.flush()

    async def get_all_active(self) -> List[Person]:
        """Get all active persons (for face recognition cache)."""
        result = await self._session.execute(
            select(Person).where(Person.is_active == True)  # noqa: E712
        )
        return list(result.scalars().all())
