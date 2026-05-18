from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.exceptions import NotFoundError

from ..dependencies import get_db
from ..models.follow import Follow
from ..models.post import Post
from ..models.user import User
from ..schemas.follow import FollowCreate, FollowRead
from ..schemas.post import PostRead
from ..schemas.user import UserCreate, UserRead

router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(
        username=body.username,
        avatar_url=body.avatar_url,
        bio=body.bio,
        location=body.location,
        tags=body.tags,
        is_agent=body.is_agent,
        agent_id=body.agent_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


@router.get("/users/{user_id}/posts", response_model=list[PostRead])
async def get_user_posts(
    user_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Post)
        .where(Post.author_id == user_id, Post.depth == 0, Post.status == "published")
        .order_by(Post.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/users/{user_id}/followers", response_model=list[UserRead])
async def get_followers(
    user_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(User)
        .join(Follow, Follow.follower_id == User.id)
        .where(Follow.followee_id == user_id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/users/{user_id}/following", response_model=list[UserRead])
async def get_following(
    user_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(User)
        .join(Follow, Follow.followee_id == User.id)
        .where(Follow.follower_id == user_id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/users/{user_id}/follow", response_model=FollowRead)
async def follow_user(
    user_id: uuid.UUID,
    body: FollowCreate,
    db: AsyncSession = Depends(get_db),
):
    if body.follower_id == user_id:
        raise NotFoundError("Cannot follow yourself")

    target = await db.get(User, user_id)
    if not target:
        raise NotFoundError("User not found")

    follower = await db.get(User, body.follower_id)
    if not follower:
        raise NotFoundError("Follower not found")

    follow = Follow(follower_id=body.follower_id, followee_id=user_id)
    db.add(follow)

    target.follower_count += 1
    follower.following_count += 1

    await db.commit()
    await db.refresh(follow)
    return follow
