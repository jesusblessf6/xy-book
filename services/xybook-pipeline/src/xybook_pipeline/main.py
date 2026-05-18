from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.router import api_router
from .config import get_settings

_heat_sync_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _heat_sync_task

    settings = get_settings()

    from xybook_common.redis_client import get_redis_pool
    redis = get_redis_pool(settings.redis_url)
    app.state.redis = redis

    from xybook_common.db.session import create_session_factory
    session_factory = create_session_factory(settings.database_url)
    app.state.session_factory = session_factory

    from xybook_common.clients.community_client import CommunityClient
    community = CommunityClient(base_url=settings.community_url)
    app.state.community = community

    from .services.heat_sync import run_heat_sync
    _heat_sync_task = asyncio.create_task(
        run_heat_sync(redis, session_factory, interval_seconds=300)
    )

    yield

    if _heat_sync_task:
        _heat_sync_task.cancel()
        try:
            await _heat_sync_task
        except asyncio.CancelledError:
            pass
    await community.close()
    await redis.aclose()


def create_app() -> FastAPI:
    app = FastAPI(title="XY-Book Pipeline Service", version="0.1.0")
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "pipeline"}

    return app


app = create_app()
