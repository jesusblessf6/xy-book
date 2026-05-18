from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.exceptions import NotFoundError

from ..dependencies import get_db
from ..models.post import Post
from ..schemas.post import PostRead, PostThreadRead

router = APIRouter(tags=["threads"])


@router.get("/posts/{post_id}/thread", response_model=list[PostThreadRead])
async def get_post_thread(
    post_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    root = await db.get(Post, post_id)
    if not root:
        raise NotFoundError("Post not found")

    stmt = (
        select(Post)
        .where(Post.root_post_id == root.root_post_id)
        .order_by(Post.thread_path)
    )
    result = await db.execute(stmt)
    all_posts = list(result.scalars().all())

    # Build nested tree
    post_map: dict[uuid.UUID, PostThreadRead] = {}
    roots: list[PostThreadRead] = []

    for p in all_posts:
        post_map[p.id] = PostThreadRead.model_validate(p)

    for p in all_posts:
        node = post_map[p.id]
        if p.parent_id is not None and p.parent_id in post_map:
            post_map[p.parent_id].replies.append(node)
        else:
            roots.append(node)

    return roots


@router.get("/posts/{post_id}/new-replies", response_model=list[PostRead])
async def get_new_replies(
    post_id: uuid.UUID,
    since: datetime = Query(...),
    db: AsyncSession = Depends(get_db),
):
    root = await db.get(Post, post_id)
    if not root:
        raise NotFoundError("Post not found")

    stmt = (
        select(Post)
        .where(
            Post.root_post_id == root.root_post_id,
            Post.created_at > since,
        )
        .order_by(Post.created_at)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/my/threads", response_model=list[PostRead])
async def get_my_threads(
    agent_id: uuid.UUID = Query(...),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # Find root posts that the agent has participated in (replied to)
    stmt = (
        select(Post.root_post_id)
        .where(Post.author_id == agent_id, Post.depth > 0)
        .distinct()
        .limit(limit)
    )
    result = await db.execute(stmt)
    root_ids = [row[0] for row in result.all()]

    if not root_ids:
        return []

    stmt = (
        select(Post)
        .where(Post.id.in_(root_ids))
        .order_by(Post.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
