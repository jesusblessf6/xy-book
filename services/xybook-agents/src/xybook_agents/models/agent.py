import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class Agent(TimestampMixin, Base):
    __tablename__ = "agents"

    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False, unique=True, index=True)
    persona_archetype: Mapped[str] = mapped_column(String(100), nullable=False)
    persona_variant: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="idle", index=True)
    last_browsed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    next_browse_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    persona_config: Mapped[dict] = mapped_column(JSONB, nullable=False)
