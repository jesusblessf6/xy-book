from __future__ import annotations

import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db, get_redis
from ..models.post import Post
from ..schemas.post import HotPostRead, PostRead

router = APIRouter(tags=["feed"])


@router.get("/feed", response_model=list[PostRead])
async def get_feed(
    sort: str = Query("latest", pattern="^(latest|hot|following)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Post).where(Post.status == "published", Post.depth == 0)

    if sort == "latest":
        stmt = stmt.order_by(Post.created_at.desc())
    elif sort == "hot":
        stmt = stmt.order_by(Post.created_at.desc())
    # following: TODO: needs user context

    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/posts/hot", response_model=list[HotPostRead])
async def get_hot_posts(
    since: str | None = None,
    limit: int = Query(10, ge=1, le=100),
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        redis = get_redis()
    except RuntimeError:
        redis = None

    stmt = select(Post).where(Post.status == "published", Post.depth == 0)
    if category:
        stmt = stmt.where(Post.category == category)

    result = await db.execute(stmt)
    posts = list(result.scalars().all())

    now = datetime.now(timezone.utc)
    scored: list[tuple[float, HotPostRead]] = []

    for p in posts:
        engagement = p.likes_count * 1.0 + p.comments_count * 3.0 + p.reposts_count * 2.0
        age_hours = (now - p.created_at.replace(tzinfo=timezone.utc)).total_seconds() / 3600
        decay = math.exp(-0.693 * age_hours / 24) if age_hours > 0 else 1.0

        event_heat = 0.0
        if redis:
            val = await redis.get(f"post:{p.id}:event_heat")
            if val:
                event_heat = float(val)

        boost = 1.0 + event_heat
        heat_score = engagement * boost * decay

        hr = HotPostRead.model_validate(p)
        hr.heat_score = heat_score
        scored.append((heat_score, hr))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:limit]]
