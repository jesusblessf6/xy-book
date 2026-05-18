from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    persona_archetype: str
    username: str | None = None
    bio: str | None = None


class BatchCreateRequest(BaseModel):
    persona_archetype: str
    count: int = Field(default=3, ge=1, le=20)
    username_prefix: str | None = None


class AgentRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    persona_archetype: str
    persona_variant: int
    status: str
    last_browsed_at: datetime | None
    last_posted_at: datetime | None
    next_browse_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
