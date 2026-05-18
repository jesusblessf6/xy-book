from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..models.post import Post
from ..schemas.post import PostRead

router = APIRouter(tags=["search"])


@router.get("/search", response_model=list[PostRead])
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    pattern = f"%{q}%"
    stmt = (
        select(Post)
        .where(
            Post.status == "published",
            Post.depth == 0,
            or_(
                Post.content.ilike(pattern),
                Post.title.ilike(pattern),
            ),
        )
        .order_by(Post.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
