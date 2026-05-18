"""Tests for persona templates and variant instantiation."""

from xybook_agents.personas.templates import ARCHETYPES
from xybook_agents.personas.variants import instantiate_persona


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


def test_instantiate_persona_variant():
    base = ARCHETYPES["数据辩手"]
    v0 = instantiate_persona("数据辩手", 0)
    v1 = instantiate_persona("数据辩手", 1)

    # Should be same archetype name
    assert v0.name == base.name
    assert v1.name == base.name

    # Variants have perturbed probabilities (±15%), still in valid range
    for v in (v0, v1):
        assert 0 <= v.behavior.like_probability <= 1
        assert 0 <= v.behavior.reply_probability <= 1
        assert 0 <= v.behavior.repost_probability <= 1


def test_instantiate_persona_roundtrip():
    persona = instantiate_persona("情绪化反驳者", 3)
    d = persona.to_dict()
    from xybook_common.persona import PersonaArchetype
    restored = PersonaArchetype.from_dict(d)
    assert restored.name == persona.name
    assert restored.behavior.reply_probability == persona.behavior.reply_probability
