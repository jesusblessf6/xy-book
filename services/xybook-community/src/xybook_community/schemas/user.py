from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    avatar_url: str | None
    bio: str | None
    location: str | None
    tags: list[str]
    following_count: int
    follower_count: int
    post_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    username: str
    avatar_url: str | None = None
    bio: str | None = None
    location: str | None = None
    tags: list[str] = Field(default_factory=list)
    is_agent: bool = True
    agent_id: str | None = None
