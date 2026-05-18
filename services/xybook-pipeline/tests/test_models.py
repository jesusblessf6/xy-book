from xybook_pipeline.models.event import Event
from xybook_pipeline.models.event_post_mapping import EventPostMapping


def test_event_table():
    assert Event.__tablename__ == "events"
    assert "category" in Event.__table__.c
    assert "intensity" in Event.__table__.c
    assert "status" in Event.__table__.c
    assert "tags" in Event.__table__.c
    assert Event.__table__.c.tags.type.__class__.__name__ == "JSONB"


def test_event_post_mapping_table():
    assert EventPostMapping.__tablename__ == "event_post_mappings"
    assert "event_id" in EventPostMapping.__table__.c
    assert "post_id" in EventPostMapping.__table__.c
