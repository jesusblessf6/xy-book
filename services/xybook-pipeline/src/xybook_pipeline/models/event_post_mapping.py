import uuid
from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class EventPostMapping(TimestampMixin, Base):
    __tablename__ = "event_post_mappings"

    event_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    post_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("event_id", "post_id", name="uq_event_post"),
    )
