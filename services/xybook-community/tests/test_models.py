import uuid

from xybook_community.models.follow import Follow
from xybook_community.models.notification import Notification
from xybook_community.models.post import Post
from xybook_community.models.read_state import ReadState
from xybook_community.models.user import User


def test_user_table():
    assert User.__tablename__ == "users"
    assert "username" in User.__table__.c
    assert "is_agent" in User.__table__.c
    assert "agent_id" in User.__table__.c
    assert User.__table__.c.tags.type.__class__.__name__ == "JSONB"


def test_post_table():
    assert Post.__tablename__ == "posts"
    assert "root_post_id" in Post.__table__.c
    assert "depth" in Post.__table__.c
    assert "thread_path" in Post.__table__.c
    assert "emotion_primary" in Post.__table__.c
    assert "emotion_intensity" in Post.__table__.c
    assert Post.__table__.c.tags.type.__class__.__name__ == "JSONB"
    assert Post.__table__.c.media.type.__class__.__name__ == "JSONB"


def test_follow_table():
    assert Follow.__tablename__ == "follows"
    assert "follower_id" in Follow.__table__.c
    assert "followee_id" in Follow.__table__.c
    pks = [c.name for c in Follow.__table__.primary_key.columns]
    assert "follower_id" in pks
    assert "followee_id" in pks


def test_notification_table():
    assert Notification.__tablename__ == "notifications"
    assert "user_id" in Notification.__table__.c
    assert "type" in Notification.__table__.c
    assert "read" in Notification.__table__.c


def test_read_state_table():
    assert ReadState.__tablename__ == "read_states"
    assert "agent_id" in ReadState.__table__.c
    assert "post_id" in ReadState.__table__.c
