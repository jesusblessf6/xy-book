from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.router import api_router
from .config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="XY-Book Experiment Service", version="0.1.0")
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "experiments"}

    return app


app = create_app()
