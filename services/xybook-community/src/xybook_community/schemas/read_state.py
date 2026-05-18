import uuid
from datetime import datetime

from pydantic import BaseModel

from xybook_common.enums import InteractionType


class ReadStateCreate(BaseModel):
    agent_id: uuid.UUID
    post_id: uuid.UUID


class ReadStateRead(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    post_id: uuid.UUID
    seen_at: datetime
    last_checked_at: datetime
    has_interacted: bool
    interaction_type: str | None

    model_config = {"from_attributes": True}
