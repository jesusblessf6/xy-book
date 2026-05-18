import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    from_user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    post_id: Mapped[uuid.UUID | None] = mapped_column()
    read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    __table_args__ = (
        Index("ix_notifications_user_read", "user_id", "read", "created_at"),
    )
