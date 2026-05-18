import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class Event(TimestampMixin, Base):
    __tablename__ = "events"

    post_type: Mapped[str | None] = mapped_column(String(20))
    source_author: Mapped[str | None] = mapped_column(String(200))
    source_platform: Mapped[str | None] = mapped_column(String(50))
    source_url: Mapped[str | None] = mapped_column(String(500))
    source_content: Mapped[str | None] = mapped_column(Text)
    source_media: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    source_metrics: Mapped[dict | None] = mapped_column(JSONB)
    direct_content: Mapped[str | None] = mapped_column(Text)
    operator_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    operator_comment: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    tags: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    intensity: Mapped[str] = mapped_column(String(20), nullable=False, default="medium", server_default="medium")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft", server_default="draft", index=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
