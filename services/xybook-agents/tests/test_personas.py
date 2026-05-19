"""Tests for persona templates, variant pools, and variant instantiation."""

from xybook_agents.personas.templates import ARCHETYPES
from xybook_agents.personas.variant_pools import VARIANT_SLOTS, VariantSlot
from xybook_agents.personas.variants import generate_username, instantiate_persona
from xybook_common.persona import PersonaArchetype


def test_archetypes_exist():
    assert "数据辩手" in ARCHETYPES
    assert "情绪化反驳者" in ARCHETYPES
    assert "佛系旁观者" in ARCHETYPES


def test_archetype_fields():
    for name, archetype in ARCHETYPES.items():
        assert archetype.name == name
        assert len(archetype.core_traits) > 0
        assert archetype.browsing.pattern in ("scheduled", "frequent", "random", "lurker", "searcher")
        assert 0 <= archetype.behavior.like_probability <= 1
        assert 0 <= archetype.behavior.reply_probability <= 1
        assert 0 <= archetype.behavior.repost_probability <= 1


def test_data_debater_traits():
    d = ARCHETYPES["数据辩手"]
    assert d.behavior.reply_probability >= 0.5
    assert d.cognitive.confrontation_style == "data_driven"


def test_emotional_rebuttor_traits():
    e = ARCHETYPES["情绪化反驳者"]
    assert e.browsing.pattern == "frequent"
    assert e.behavior.reply_probability >= 0.6
    assert e.cognitive.confrontation_style == "counterattack"


def test_zen_observer_traits():
    z = ARCHETYPES["佛系旁观者"]
    assert z.behavior.like_probability >= 0.35
    assert z.behavior.reply_probability <= 0.15
    assert z.cognitive.confrontation_style == "withdraw"


def test_variant_pools_defined():
    for name in ARCHETYPES:
        assert name in VARIANT_SLOTS
        assert len(VARIANT_SLOTS[name]) >= 6
        for slot in VARIANT_SLOTS[name]:
            assert isinstance(slot, VariantSlot)
            assert len(slot.variant_name) > 0
            assert len(slot.variant_bio) > 0
            assert len(slot.typical_phrases) >= 2


def test_instantiate_persona_variant_has_identity():
    p0 = instantiate_persona("数据辩手", 0)
    assert p0.variant_name == "林锐"
    assert "北京" in p0.variant_bio
    assert p0.language_style.tone == "academic_precise"


def test_instantiate_persona_different_variants_differ():
    p0 = instantiate_persona("数据辩手", 0)
    p1 = instantiate_persona("数据辩手", 1)
    assert p0.variant_name != p1.variant_name
    assert p0.variant_bio != p1.variant_bio
    assert p0.language_style.tone != p1.language_style.tone
    assert p0.language_style.typical_phrases != p1.language_style.typical_phrases
    assert p0.browsing.viewing_strategy.follow != p1.browsing.viewing_strategy.follow


def test_instantiate_persona_variant_probabilities_valid():
    for name in ARCHETYPES:
        for vid in range(12):
            p = instantiate_persona(name, vid)
            assert 0 <= p.behavior.like_probability <= 1, f"{name} v{vid} like={p.behavior.like_probability}"
            assert 0 <= p.behavior.reply_probability <= 1, f"{name} v{vid} reply={p.behavior.reply_probability}"
            assert 0 <= p.behavior.repost_probability <= 1, f"{name} v{vid} repost={p.behavior.repost_probability}"
            assert 0 <= p.emotion_patterns.aggression <= 1
            assert 0 <= p.emotion_patterns.sarcasm <= 1


def test_instantiate_persona_roundtrip():
    persona = instantiate_persona("情绪化反驳者", 3)
    d = persona.to_dict()
    assert "variant_name" in d
    assert "variant_bio" in d
    restored = PersonaArchetype.from_dict(d)
    assert restored.variant_name == persona.variant_name
    assert restored.variant_bio == persona.variant_bio
    assert restored.language_style.tone == persona.language_style.tone


def test_instantiate_persona_slot_roundrobin():
    # variant_id 6 should wrap around to slot 0
    p0 = instantiate_persona("数据辩手", 0)
    p6 = instantiate_persona("数据辩手", 6)
    assert p6.variant_name == p0.variant_name
    # But they should have slightly different probabilities (random perturbation)
    # Can't guarantee they differ due to randomness, but structure should be same


def test_generate_username():
    name = generate_username("林锐", "数据辩手")
    assert "林锐" in name
    assert "数据" in name

    name2 = generate_username("吴昊", "情绪化反驳者")
    assert "吴昊" in name2
    assert "说真话" in name2


def test_backward_compat_no_variant_fields():
    old_data = {"name": "test", "core_traits": ["a"], "demographics": "test"}
    p = PersonaArchetype.from_dict(old_data)
    assert p.variant_name == ""
    assert p.variant_bio == ""
