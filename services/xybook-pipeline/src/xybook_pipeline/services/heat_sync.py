"""Background task to sync event heat scores to Redis."""

from __future__ import annotations

import asyncio
import logging
import math
from datetime import datetime, timezone

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from xybook_common.enums import EventStatus

from ..models.event import Event
from ..models.event_post_mapping import EventPostMapping

logger = logging.getLogger(__name__)

HALF_LIFE_HOURS = 6.0  # Event heat decays with 6-hour half-life
HEAT_EXPIRED_THRESHOLD = 0.01


def compute_event_heat(activated_at: datetime, now: datetime) -> float:
    """Exponential decay: heat = e^(-ln(2) * hours_since_activation / half_life)."""
    hours_elapsed = (now - activated_at).total_seconds() / 3600
    if hours_elapsed < 0:
        return 1.0
    return math.exp(-math.log(2) * hours_elapsed / HALF_LIFE_HOURS)


async def run_heat_sync(
    redis: Redis,
    session_factory: async_sessionmaker[AsyncSession],
    interval_seconds: int = 300,
) -> None:
    """Periodically sync event heat scores to Redis and expire cold events."""
    logger.info("Heat sync started (interval=%ds)", interval_seconds)

    while True:
        try:
            now = datetime.now(timezone.utc)
            async with session_factory() as db:
                stmt = select(Event).where(Event.status == EventStatus.ACTIVE)
                result = await db.execute(stmt)
                events = list(result.scalars().all())

                for event in events:
                    if not event.activated_at:
                        continue

                    heat = compute_event_heat(event.activated_at, now)

                    # Find the post for this event
                    mapping_stmt = select(EventPostMapping).where(
                        EventPostMapping.event_id == event.id
                    )
                    mapping_result = await db.execute(mapping_stmt)
                    mapping = mapping_result.scalar_one_or_none()

                    if mapping:
                        key = f"post:{mapping.post_id}:event_heat"
                        if heat < HEAT_EXPIRED_THRESHOLD:
                            await redis.delete(key)
                            event.status = EventStatus.EXPIRED
                            logger.info(
                                "Event %s expired (heat=%.4f)", event.id, heat
                            )
                        else:
                            await redis.set(key, str(heat))
                            await redis.expire(key, int(HALF_LIFE_HOURS * 3600 * 2))

                await db.commit()

        except asyncio.CancelledError:
            logger.info("Heat sync cancelled")
            return
        except Exception as e:
            logger.error("Heat sync error: %s", e)

        await asyncio.sleep(interval_seconds)
