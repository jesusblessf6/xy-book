from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.router import router
from .middleware.auth import AuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="XY-Book API Gateway", version="0.1.0")
    app.add_middleware(AuthMiddleware)

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "gateway"}

    app.include_router(router)

    return app


app = create_app()
