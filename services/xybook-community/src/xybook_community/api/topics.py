from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.enums import PostCategory

from ..dependencies import get_db
from ..models.post import Post
from ..schemas.post import PostRead

router = APIRouter(tags=["topics"])


@router.get("/topics")
async def get_topics():
    return [{"id": c.value, "name": c.value} for c in PostCategory]


@router.get("/topics/{topic_id}/posts", response_model=list[PostRead])
async def get_topic_posts(
    topic_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Post)
        .where(Post.category == topic_id, Post.status == "published", Post.depth == 0)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
