"""
Detection event repository — batched insertion of detection snapshots.

Events are collected in-memory and flushed periodically to
prevent excessive database writes during real-time processing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.models.detection_event import DetectionEvent

logger = get_logger(__name__)


class EventRepository:
    """Repository for detection event operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_batch(self, events: List[dict]) -> int:
        """
        Batch insert detection events.

        Args:
            events: List of event dictionaries matching DetectionEvent columns.

        Returns:
            Number of events inserted.
        """
        if not events:
            return 0

        db_events = [DetectionEvent(**event) for event in events]
        self._session.add_all(db_events)
        await self._session.flush()
        logger.info("Detection events batch inserted", count=len(db_events))
        return len(db_events)

    async def get_recent(
        self,
        limit: int = 100,
        person_id: Optional[UUID] = None,
    ) -> List[DetectionEvent]:
        """Get recent detection events, optionally filtered by person."""
        query = select(DetectionEvent).order_by(DetectionEvent.timestamp.desc())

        if person_id:
            query = query.where(DetectionEvent.person_id == person_id)

        query = query.limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_count(self, person_id: Optional[UUID] = None) -> int:
        """Get total count of detection events."""
        query = select(func.count(DetectionEvent.id))
        if person_id:
            query = query.where(DetectionEvent.person_id == person_id)
        result = await self._session.execute(query)
        return result.scalar() or 0

    async def cleanup_old_events(self, retention_days: int) -> int:
        """Delete detection events older than retention period."""
        if retention_days <= 0:
            return 0

        cutoff = datetime.now(timezone.utc) - __import__("datetime").timedelta(days=retention_days)
        result = await self._session.execute(
            delete(DetectionEvent).where(DetectionEvent.timestamp < cutoff)
        )
        await self._session.flush()
        count = result.rowcount
        if count > 0:
            logger.info("Old detection events cleaned up", count=count, retention_days=retention_days)
        return count
