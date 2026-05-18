import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from xybook_common.enums import EmotionType, PostCategory, PostStatus, PostType


class PostCreate(BaseModel):
    author_id: uuid.UUID
    title: str | None = None
    content: str
    media: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    category: PostCategory | None = None
    post_type: PostType | None = None
    parent_id: uuid.UUID | None = None
    root_post_id: uuid.UUID | None = None
    scheduled_at: datetime | None = None


class PostRead(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    title: str | None
    content: str
    media: list[str]
    tags: list[str]
    category: str | None
    post_type: str | None
    status: str
    likes_count: int
    comments_count: int
    reposts_count: int
    parent_id: uuid.UUID | None
    root_post_id: uuid.UUID
    depth: int
    thread_path: str
    emotion_primary: str | None
    emotion_intensity: float
    controversy_score: float
    created_at: datetime

    model_config = {"from_attributes": True}


class PostThreadRead(PostRead):
    replies: list["PostThreadRead"] = []

    model_config = {"from_attributes": True}


class HotPostRead(PostRead):
    heat_score: float = 0.0

    model_config = {"from_attributes": True}
