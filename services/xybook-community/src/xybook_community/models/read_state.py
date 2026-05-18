import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class ReadState(TimestampMixin, Base):
    __tablename__ = "read_states"

    agent_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    post_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    has_interacted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    interaction_type: Mapped[str | None] = mapped_column(String(20))

    __table_args__ = (
        UniqueConstraint("agent_id", "post_id", name="uq_read_states_agent_post"),
    )
