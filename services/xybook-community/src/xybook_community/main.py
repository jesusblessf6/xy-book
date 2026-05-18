from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.router import api_router
from .config import get_settings
from .dependencies import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()


def create_app() -> FastAPI:
    app = FastAPI(title="XY-Book Community Service", version="0.1.0")
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "community"}

    return app


app = create_app()
