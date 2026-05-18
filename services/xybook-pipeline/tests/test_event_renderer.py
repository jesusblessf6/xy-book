"""Tests for event content rendering and heat computation."""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from xybook_pipeline.services.event_renderer import render_post_content
from xybook_pipeline.services.heat_sync import compute_event_heat


def _make_event(**kwargs):
    defaults = {
        "post_type": "original",
        "source_author": None,
        "source_platform": None,
        "source_content": None,
        "direct_content": "直接发布的内容",
        "operator_comment": None,
    }
    defaults.update(kwargs)
    event = MagicMock()
    for k, v in defaults.items():
        setattr(event, k, v)
    return event


def test_render_original_post():
    event = _make_event(post_type="original", direct_content="这是原创内容")
    content = render_post_content(event)
    assert "这是原创内容" in content


def test_render_repost():
    event = _make_event(
        post_type="repost",
        source_author="张三",
        source_platform="微博",
        source_content="原始帖子内容",
        operator_comment="我的评论",
        direct_content=None,
    )
    content = render_post_content(event)
    assert "张三" in content
    assert "微博" in content
    assert "原始帖子内容" in content
    assert "我的评论" in content


def test_render_mixed():
    event = _make_event(
        post_type="mixed",
        source_author="李四",
        source_platform="豆瓣",
        source_content="来源内容",
        direct_content="自己的话",
        operator_comment=None,
    )
    content = render_post_content(event)
    assert "李四" in content
    assert "来源内容" in content
    assert "自己的话" in content


def test_render_empty_content():
    event = _make_event(
        post_type=None,
        source_content=None,
        direct_content=None,
        operator_comment=None,
    )
    content = render_post_content(event)
    assert len(content) > 0


def test_compute_event_heat_fresh():
    now = datetime.now(timezone.utc)
    activated = now - timedelta(minutes=1)
    heat = compute_event_heat(activated, now)
    assert 0.9 < heat <= 1.0


def test_compute_event_heat_half_life():
    now = datetime.now(timezone.utc)
    activated = now - timedelta(hours=6)
    heat = compute_event_heat(activated, now)
    assert 0.45 < heat < 0.55  # ~0.5 at half-life


def test_compute_event_heat_cold():
    now = datetime.now(timezone.utc)
    activated = now - timedelta(hours=48)
    heat = compute_event_heat(activated, now)
    assert heat < 0.01


def test_compute_event_heat_future():
    now = datetime.now(timezone.utc)
    activated = now + timedelta(hours=1)
    heat = compute_event_heat(activated, now)
    assert heat == 1.0
