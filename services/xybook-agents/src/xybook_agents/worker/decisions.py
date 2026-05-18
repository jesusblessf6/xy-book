from __future__ import annotations

import math
import random
from datetime import datetime, timedelta, timezone

from xybook_common.persona import PersonaArchetype


def decide_action(persona: PersonaArchetype, post: dict) -> str:
    """Decide what action to take on a post. Returns: like, reply, repost, or silent."""
    silence_prob = _predict_silence(persona, post)
    if random.random() < silence_prob:
        return "silent"

    p_like = persona.behavior.like_probability
    p_reply = persona.behavior.reply_probability
    p_repost = persona.behavior.repost_probability

    # Arousal adjustment
    arousal = compute_arousal(persona, post)
    if arousal > 0.7:
        p_reply *= 1.5
        p_like *= 0.5
    elif arousal < 0.2:
        p_like *= 1.5

    # Normalize and sample
    total = p_like + p_reply + p_repost
    r = random.random() * total
    if r < p_like:
        return "like"
    elif r < p_like + p_reply:
        return "reply"
    else:
        return "repost"


def compute_arousal(persona: PersonaArchetype, post: dict) -> float:
    """Compute emotional arousal based on persona triggers and post content."""
    arousal = 0.0
    content = post.get("content", "")

    for trigger in persona.emotion_patterns.triggers:
        if trigger.keyword in content:
            arousal += trigger.intensity_increment

    # Post emotion intensity
    arousal += post.get("emotion_intensity", 0.0) * 0.3

    # Individual reactivity
    arousal *= persona.cognitive.emotional_reactivity

    return min(arousal, 1.0)


def compute_delay(persona: PersonaArchetype, action: str, post: dict) -> float:
    """Return delay in seconds before executing action."""
    base_minutes = persona.browsing.avg_response_delay_minutes

    type_modifier = {"like": 0.5, "repost": 0.8, "reply": 1.0}
    mod = type_modifier.get(action, 1.0)

    arousal = compute_arousal(persona, post)
    arousal_modifier = 1.0 - (arousal * 0.5)

    delay_minutes = base_minutes * mod * arousal_modifier
    jitter = random.uniform(0.5, 2.0)

    return max(0.1, delay_minutes * jitter * 60)


def filter_by_interest(persona: PersonaArchetype, posts: list[dict]) -> list[dict]:
    """Filter posts based on persona's interest and browsing strategy."""
    vs = persona.browsing.viewing_strategy
    filtered = []

    for post in posts:
        category = post.get("category")

        # Ignore list
        if category and category in vs.ignore:
            continue

        # Scroll behavior
        if vs.scroll_behavior == "selective":
            if category and vs.follow and category not in vs.follow:
                continue
        # skim: skip based on title (simplified — just pass through for mock)
        # thorough: pass all

        filtered.append(post)

    return filtered


def should_check_my_threads(persona: PersonaArchetype) -> bool:
    """Whether agent should check threads they've participated in."""
    return random.random() < persona.behavior.thread_tracking_tendency


def compute_next_browse_time(persona: PersonaArchetype) -> datetime:
    """Compute when the agent should next browse."""
    now = datetime.now(timezone.utc)

    if persona.browsing.pattern == "frequent":
        # Poisson process: interval between sessions
        rate = persona.browsing.session_frequency / 24  # per hour
        if rate > 0:
            interval_minutes = random.expovariate(rate) * 60
        else:
            interval_minutes = 60
        return now + timedelta(minutes=max(1, interval_minutes))

    elif persona.browsing.pattern == "scheduled":
        # Next peak hour
        current_hour = now.hour
        peak_hours = sorted(persona.browsing.peak_hours)
        for h in peak_hours:
            if h > current_hour:
                target = now.replace(hour=h, minute=random.randint(0, 30), second=0)
                return target
        # Next day first peak
        next_day = now + timedelta(days=1)
        return next_day.replace(
            hour=peak_hours[0], minute=random.randint(0, 30), second=0
        )

    else:  # random, lurker, searcher
        return now + timedelta(minutes=random.randint(30, 180))


def _predict_silence(persona: PersonaArchetype, post: dict) -> float:
    """Predict probability of silence for this agent on this post."""
    p = persona.silence_patterns.base_silence_ratio

    category = post.get("category")
    vs = persona.browsing.viewing_strategy

    if category and vs.follow and category in vs.follow:
        p *= persona.silence_patterns.topic_match_multiplier
    elif category and vs.ignore and category in vs.ignore:
        p *= persona.silence_patterns.topic_mismatch_multiplier
    else:
        # Category not in follow or ignore — moderate silence
        p *= 1.5

    # High engagement posts reduce silence
    engagement = (post.get("likes_count", 0) + post.get("comments_count", 0) * 3
                  + post.get("reposts_count", 0) * 2)
    if engagement > 100:
        p *= 0.7

    return max(0.05, min(0.98, p))
