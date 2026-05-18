import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from xybook_common.enums import EventIntensity, EventStatus, PostType


class EventCreate(BaseModel):
    post_type: PostType | None = None
    source_author: str | None = None
    source_platform: str | None = None
    source_url: str | None = None
    source_content: str | None = None
    source_media: list[str] = Field(default_factory=list)
    source_metrics: dict | None = None
    direct_content: str | None = None
    operator_id: uuid.UUID
    operator_comment: str | None = None
    category: str
    tags: list[str] = Field(default_factory=list)
    intensity: EventIntensity = EventIntensity.MEDIUM
    scheduled_at: datetime | None = None


class EventUpdate(BaseModel):
    post_type: PostType | None = None
    source_author: str | None = None
    source_content: str | None = None
    operator_comment: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    intensity: EventIntensity | None = None
    scheduled_at: datetime | None = None


class EventRead(BaseModel):
    id: uuid.UUID
    post_type: str | None
    source_author: str | None
    source_platform: str | None
    source_url: str | None
    source_content: str | None
    source_media: list
    source_metrics: dict | None
    direct_content: str | None
    operator_id: uuid.UUID
    operator_comment: str | None
    category: str
    tags: list
    intensity: str
    status: str
    scheduled_at: datetime | None
    activated_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
