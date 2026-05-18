from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.exceptions import NotFoundError

from ..dependencies import get_db
from ..models.notification import Notification
from ..models.post import Post
from ..models.read_state import ReadState
from ..schemas.interaction import LikeRequest, LikeResponse, RepostRequest, RepostResponse
from ..schemas.post import PostRead

router = APIRouter(tags=["interactions"])


@router.post("/posts/{post_id}/like", response_model=LikeResponse)
async def like_post(
    post_id: uuid.UUID, body: LikeRequest, db: AsyncSession = Depends(get_db)
):
    post = await db.get(Post, post_id)
    if not post:
        raise NotFoundError("Post not found")

    post.likes_count += 1

    # Create notification for post author
    if post.author_id != body.user_id:
        n = Notification(
            user_id=post.author_id, type="like",
            from_user_id=body.user_id, post_id=post.id,
        )
        db.add(n)

    # Update read state if exists
    stmt = (
        update(ReadState)
        .where(ReadState.agent_id == body.user_id, ReadState.post_id == post_id)
        .values(has_interacted=True, interaction_type="like")
    )
    await db.execute(stmt)

    await db.commit()
    return LikeResponse(post_id=post.id, likes_count=post.likes_count)


@router.post("/posts/{post_id}/repost", response_model=RepostResponse)
async def repost_post(
    post_id: uuid.UUID, body: RepostRequest, db: AsyncSession = Depends(get_db)
):
    original = await db.get(Post, post_id)
    if not original:
        raise NotFoundError("Post not found")

    original.reposts_count += 1

    repost = Post(
        author_id=body.user_id,
        content=body.content or f"转发: {original.content[:100]}",
        post_type="repost",
        category=original.category,
        tags=original.tags,
        parent_id=original.id,
        root_post_id=repost.id if True else original.root_post_id,
        depth=0,
        thread_path="",
    )
    # Repost is a new root post
    repost.root_post_id = repost.id
    repost.thread_path = str(repost.id)

    db.add(repost)

    # Create notification for original author
    if original.author_id != body.user_id:
        n = Notification(
            user_id=original.author_id, type="repost",
            from_user_id=body.user_id, post_id=original.id,
        )
        db.add(n)

    await db.commit()
    await db.refresh(repost)
    return RepostResponse(post=PostRead.model_validate(repost))
