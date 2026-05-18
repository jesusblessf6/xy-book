import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    bio: Mapped[str | None] = mapped_column(String(1000))
    location: Mapped[str | None] = mapped_column(String(200))
    tags: Mapped[list] = mapped_column(JSONB, default=list, server_default="[]")
    following_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    follower_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    post_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_agent: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    agent_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
