from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class FollowCreate(BaseModel):
    follower_id: uuid.UUID
    followee_id: uuid.UUID


class FollowRead(BaseModel):
    follower_id: uuid.UUID
    followee_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
