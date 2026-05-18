from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings


_session_factory = None


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
