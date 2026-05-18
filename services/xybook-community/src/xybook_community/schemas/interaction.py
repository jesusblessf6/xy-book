from __future__ import annotations

import uuid

from pydantic import BaseModel

from .post import PostRead


class LikeRequest(BaseModel):
    user_id: uuid.UUID


class LikeResponse(BaseModel):
    post_id: uuid.UUID
    likes_count: int


class RepostRequest(BaseModel):
    user_id: uuid.UUID
    content: str | None = None


class RepostResponse(BaseModel):
    post: PostRead
