from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class NotificationRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    type: str
    from_user_id: uuid.UUID
    post_id: uuid.UUID | None
    read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationMarkRead(BaseModel):
    notification_ids: list[uuid.UUID]
