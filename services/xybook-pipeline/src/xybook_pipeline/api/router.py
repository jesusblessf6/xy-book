from fastapi import APIRouter

from .events import router as events_router

api_router = APIRouter(prefix="/api/pipeline")
api_router.include_router(events_router)
