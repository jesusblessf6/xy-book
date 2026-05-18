from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.exceptions import NotFoundError

from ..dependencies import get_db
from ..models.notification import Notification
from ..models.post import Post
from ..models.read_state import ReadState
from ..schemas.post import PostCreate, PostRead

router = APIRouter(tags=["posts"])


async def _create_notification(
    db: AsyncSession, user_id: uuid.UUID, from_user_id: uuid.UUID,
    post_id: uuid.UUID, ntype: str,
):
    n = Notification(user_id=user_id, type=ntype, from_user_id=from_user_id, post_id=post_id)
    db.add(n)


@router.post("/posts", response_model=PostRead, status_code=201)
async def create_post(body: PostCreate, db: AsyncSession = Depends(get_db)):
    post = Post(
        author_id=body.author_id,
        title=body.title,
        content=body.content,
        media=body.media,
        tags=body.tags,
        category=body.category,
        post_type=body.post_type,
        parent_id=body.parent_id,
        scheduled_at=body.scheduled_at,
    )

    if body.parent_id is not None:
        parent = await db.get(Post, body.parent_id)
        if not parent:
            raise NotFoundError("Parent post not found")
        post.depth = parent.depth + 1
        post.root_post_id = parent.root_post_id
        post.thread_path = f"{parent.thread_path}.{post.id}"
        # Update comments count on parent
        parent.comments_count += 1
        # Create notification for parent author
        if parent.author_id != body.author_id:
            await _create_notification(
                db, user_id=parent.author_id, from_user_id=body.author_id,
                post_id=parent.id, ntype="reply",
            )
    else:
        post.root_post_id = post.id
        post.thread_path = str(post.id)

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise NotFoundError("Post not found")
    return post
