from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.router import api_router
from .config import get_settings
from .scheduler.agent_scheduler import AgentScheduler
from .worker.scheduler_runner import run_scheduler

_scheduler: AgentScheduler | None = None
_scheduler_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler, _scheduler_task

    settings = get_settings()

    from xybook_common.redis_client import get_redis_pool
    redis = get_redis_pool(settings.redis_url)
    _scheduler = AgentScheduler(redis)
    app.state.scheduler = _scheduler
    app.state.redis = redis

    # DB session factory
    from xybook_common.db.session import create_session_factory
    session_factory = create_session_factory(settings.database_url)
    app.state.session_factory = session_factory

    # Community client
    from xybook_common.clients.community_client import CommunityClient
    community = CommunityClient(base_url=settings.community_url)
    app.state.community = community

    # LLM
    from xybook_common.llm import MockLLMProvider
    llm = MockLLMProvider()
    app.state.llm = llm

    # Start scheduler runner
    _scheduler_task = asyncio.create_task(
        run_scheduler(_scheduler, session_factory, community, llm)
    )

    yield

    if _scheduler_task:
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass
    await community.close()
    await redis.aclose()


def create_app() -> FastAPI:
    app = FastAPI(title="XY-Book Agent Workers", version="0.1.0", lifespan=lifespan)
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        pending = await _scheduler.count_pending() if _scheduler else 0
        return {"status": "ok", "service": "agents", "pending_schedules": pending}

    return app


app = create_app()
