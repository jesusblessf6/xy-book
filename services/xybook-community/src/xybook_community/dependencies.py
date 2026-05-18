from __future__ import annotations

from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings


_session_factory = None
_redis_pool: Redis | None = None


def _get_session_factory():
    global _session_factory
    if _session_factory is None:
        from xybook_common.db.session import create_session_factory

        settings = get_settings()
        _session_factory = create_session_factory(settings.database_url)
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    from xybook_common.db.session import get_async_session

    factory = _get_session_factory()
    async for session in get_async_session(factory):
        yield session


def get_redis() -> Redis:
    global _redis_pool
    if _redis_pool is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis_pool


async def init_redis():
    global _redis_pool
    from xybook_common.redis_client import get_redis_pool

    settings = get_settings()
    _redis_pool = get_redis_pool(settings.redis_url)


async def close_redis():
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.aclose()
        _redis_pool = None
