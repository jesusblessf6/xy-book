"""Tests for agent decision functions."""

from datetime import datetime, timezone

from xybook_agents.personas.templates import ARCHETYPES
from xybook_agents.personas.variants import instantiate_persona
from xybook_agents.worker.decisions import (
    compute_arousal,
    compute_delay,
    compute_next_browse_time,
    decide_action,
    filter_by_interest,
    should_check_my_threads,
)


def _make_post(**kwargs):
    return {
        "id": "post-1",
        "content": "测试帖子",
        "category": "social",
        "likes_count": 0,
        "comments_count": 0,
        "reposts_count": 0,
        **kwargs,
    }


def test_decide_action_returns_valid():
    persona = instantiate_persona("数据辩手", 0)
    post = _make_post()
    actions = set()
    for _ in range(200):
        action = decide_action(persona, post)
        actions.add(action)
    # With enough samples, should see at least 2 different actions
    assert len(actions) >= 2
    assert actions.issubset({"like", "reply", "repost", "silent"})


def test_compute_arousal_no_triggers():
    persona = instantiate_persona("佛系旁观者", 0)
    post = _make_post(content="平淡无奇的内容")
    arousal = compute_arousal(persona, post)
    assert 0 <= arousal <= 1


def test_compute_arousal_with_trigger():
    persona = instantiate_persona("情绪化反驳者", 0)
    # Find a trigger keyword from persona
    if persona.emotion_patterns.triggers:
        keyword = persona.emotion_patterns.triggers[0].keyword
        post = _make_post(content=f"关于{keyword}的事情")
        arousal = compute_arousal(persona, post)
        assert arousal > 0


def test_compute_delay_positive():
    persona = instantiate_persona("数据辩手", 0)
    post = _make_post()
    for action in ("like", "reply", "repost"):
        delay = compute_delay(persona, action, post)
        assert delay > 0


def test_filter_by_interest():
    persona = instantiate_persona("数据辩手", 0)
    posts = [
        _make_post(id="1", category="tech"),
        _make_post(id="2", category="social"),
        _make_post(id="3", category="entertainment"),
    ]
    filtered = filter_by_interest(persona, posts)
    # Should return some posts (not crash)
    assert len(filtered) <= len(posts)


def test_filter_by_interest_ignore():
    persona = instantiate_persona("数据辩手", 0)
    # Add an ignore category
    if persona.browsing.viewing_strategy.ignore:
        ignore_cat = list(persona.browsing.viewing_strategy.ignore)[0]
        posts = [_make_post(id="1", category=ignore_cat)]
        filtered = filter_by_interest(persona, posts)
        assert len(filtered) == 0


def test_should_check_my_threads():
    persona = instantiate_persona("数据辩手", 0)
    # Just verify it returns a bool, not crash
    result = should_check_my_threads(persona)
    assert isinstance(result, bool)


def test_compute_next_browse_time_future():
    for name in ARCHETYPES:
        persona = instantiate_persona(name, 0)
        next_time = compute_next_browse_time(persona)
        assert isinstance(next_time, datetime)
        assert next_time > datetime.now(timezone.utc) - __import__("datetime").timedelta(seconds=5)
