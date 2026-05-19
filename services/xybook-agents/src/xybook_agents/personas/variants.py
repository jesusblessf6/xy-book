"""Instantiate persona variants with rich individual identity."""

from __future__ import annotations

import copy
import random

from xybook_common.persona import PersonaArchetype

from .templates import ARCHETYPES
from .variant_pools import VARIANT_SLOTS


def _clamp01(v: float) -> float:
    return max(0.0, min(1.0, v))


def instantiate_persona(archetype_name: str, variant_id: int) -> PersonaArchetype:
    """Create a variant of a persona archetype with slot-based individual identity.

    variant_id deterministically selects a VariantSlot (round-robin via modulo),
    then applies small random perturbation for intra-slot variety.
    """
    base = ARCHETYPES[archetype_name]
    persona = copy.deepcopy(base)

    # Select variant slot (deterministic by variant_id)
    slots = VARIANT_SLOTS[archetype_name]
    slot = slots[variant_id % len(slots)]

    # Apply individual identity
    persona.variant_name = slot.variant_name
    persona.variant_bio = slot.variant_bio

    # Apply language style override
    persona.language_style.tone = slot.language_tone
    persona.language_style.vocabulary = slot.vocabulary
    persona.language_style.typical_phrases = slot.typical_phrases
    persona.language_style.punctuation = slot.punctuation

    # Apply interest sub-focus
    persona.browsing.viewing_strategy.follow = slot.sub_focus

    # Apply behavioral shifts from slot
    persona.behavior.like_probability = _clamp01(
        persona.behavior.like_probability + slot.behavior_shift.like_probability_delta
    )
    persona.behavior.reply_probability = _clamp01(
        persona.behavior.reply_probability + slot.behavior_shift.reply_probability_delta
    )
    persona.behavior.repost_probability = _clamp01(
        persona.behavior.repost_probability + slot.behavior_shift.repost_probability_delta
    )

    # Apply emotion shifts
    persona.emotion_patterns.aggression = _clamp01(
        persona.emotion_patterns.aggression + slot.emotion_shift.aggression_delta
    )
    persona.emotion_patterns.sarcasm = _clamp01(
        persona.emotion_patterns.sarcasm + slot.emotion_shift.sarcasm_delta
    )

    # Small random perturbation for intra-slot variety (±10%)
    persona.behavior.like_probability = _clamp01(
        persona.behavior.like_probability * random.uniform(0.90, 1.10)
    )
    persona.behavior.reply_probability = _clamp01(
        persona.behavior.reply_probability * random.uniform(0.90, 1.10)
    )
    persona.behavior.repost_probability = _clamp01(
        persona.behavior.repost_probability * random.uniform(0.90, 1.10)
    )

    # Perturb timing
    persona.browsing.peak_hours = [
        max(0, min(23, h + random.randint(-1, 1)))
        for h in base.browsing.peak_hours
    ]
    persona.browsing.session_frequency = max(
        1, base.browsing.session_frequency + random.randint(-1, 1)
    )
    persona.browsing.avg_response_delay_minutes = max(
        5, base.browsing.avg_response_delay_minutes + random.randint(-5, 5)
    )

    return persona


_ARCHETYPE_SUFFIX: dict[str, str] = {
    "数据辩手": "数据",
    "情绪化反驳者": "说真话",
    "佛系旁观者": "闲看",
}


def generate_username(variant_name: str, archetype_name: str) -> str:
    """Generate a realistic Chinese username from variant name and archetype."""
    suffix = _ARCHETYPE_SUFFIX.get(archetype_name, "")
    digits = random.randint(10, 99)
    return f"{variant_name}{suffix}{digits}"
