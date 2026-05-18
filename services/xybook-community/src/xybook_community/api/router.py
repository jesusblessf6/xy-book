from fastapi import APIRouter

from .feed import router as feed_router
from .interactions import router as interactions_router
from .notifications import router as notifications_router
from .posts import router as posts_router
from .read_states import router as read_states_router
from .search import router as search_router
from .threads import router as threads_router
from .topics import router as topics_router
from .users import router as users_router

api_router = APIRouter(prefix="/api/community")
api_router.include_router(posts_router)
api_router.include_router(feed_router)
api_router.include_router(read_states_router)
api_router.include_router(interactions_router)
api_router.include_router(threads_router)
api_router.include_router(users_router)
api_router.include_router(notifications_router)
api_router.include_router(search_router)
api_router.include_router(topics_router)
