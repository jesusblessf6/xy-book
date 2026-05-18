import uuid

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from xybook_common.db.base import Base, TimestampMixin


class FakeModel(TimestampMixin, Base):
    __tablename__ = "test_fake"
    name: Mapped[str] = mapped_column(String(50))


def test_base_has_metadata():
    assert Base.metadata is not None


def test_timestamp_mixin_has_id():
    col = FakeModel.__table__.c.id
    assert col.primary_key
    assert col.type.python_type == uuid.UUID


def test_timestamp_mixin_has_created_at():
    col = FakeModel.__table__.c.created_at
    assert col.server_default is not None


def test_timestamp_mixin_has_updated_at():
    col = FakeModel.__table__.c.updated_at
    assert col.server_default is not None
