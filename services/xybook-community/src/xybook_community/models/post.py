import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class Post(TimestampMixin, Base):
    __tablename__ = "posts"

    author_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    media: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    tags: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    category: Mapped[str | None] = mapped_column(String(20), index=True)
    post_type: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="published", server_default="published", index=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # 互动计数
    likes_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    comments_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    reposts_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # 树形结构
    parent_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
    root_post_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    thread_path: Mapped[str] = mapped_column(String(500), nullable=False, default="", server_default="")

    # 情绪预计算
    emotion_primary: Mapped[str | None] = mapped_column(String(20))
    emotion_intensity: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    controversy_score: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")

    __table_args__ = (
        Index("ix_posts_thread", "root_post_id", "depth", "created_at"),
        Index("ix_posts_feed", "category", "status", "created_at"),
    )
