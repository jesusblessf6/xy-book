from __future__ import annotations

import copy
import random

from xybook_common.persona import PersonaArchetype

from .templates import ARCHETYPES


def instantiate_persona(archetype_name: str, variant_id: int) -> PersonaArchetype:
    """Create a variant of a persona archetype with random perturbation."""
    base = ARCHETYPES[archetype_name]
    persona = copy.deepcopy(base)

    # Perturb behavior probabilities by ±15%
    persona.behavior.like_probability *= random.uniform(0.85, 1.15)
    persona.behavior.reply_probability *= random.uniform(0.85, 1.15)
    persona.behavior.repost_probability *= random.uniform(0.85, 1.15)

    # Shift peak hours by ±2
    persona.browsing.peak_hours = [
        max(0, min(23, h + random.randint(-2, 2))) for h in base.browsing.peak_hours
    ]

    # Vary session frequency slightly
    persona.browsing.session_frequency = max(1, base.browsing.session_frequency + random.randint(-1, 1))

    # Vary response delay
    persona.browsing.avg_response_delay_minutes = max(
        5, base.browsing.avg_response_delay_minutes + random.randint(-10, 10)
    )

    return persona
