from xybook_common.persona import (
    BehaviorConfig,
    BrowsingConfig,
    CognitiveConfig,
    EmotionPatterns,
    EmotionTrigger,
    LanguageStyle,
    PersonaArchetype,
    SilencePatterns,
    ViewingStrategy,
)


def test_persona_roundtrip():
    p = PersonaArchetype(
        name="数据辩手",
        core_traits=["数据驱动", "克制"],
        language_style=LanguageStyle(tone="controlled_firm", typical_phrases=["来源呢？"]),
        cognitive=CognitiveConfig(emotional_reactivity=0.4, confrontation_style="data_driven"),
        emotion_patterns=EmotionPatterns(
            triggers=[EmotionTrigger(keyword="没有数据", emotion="contempt", intensity_increment=0.2)]
        ),
        browsing=BrowsingConfig(
            pattern="scheduled",
            peak_hours=[9, 13, 21],
            viewing_strategy=ViewingStrategy(follow=["tech", "social"], ignore=["entertainment"]),
        ),
        behavior=BehaviorConfig(like_probability=0.25, reply_probability=0.55),
        silence_patterns=SilencePatterns(base_silence_ratio=0.4),
    )
    d = p.to_dict()
    p2 = PersonaArchetype.from_dict(d)
    assert p2.name == "数据辩手"
    assert p2.cognitive.confrontation_style == "data_driven"
    assert p2.emotion_patterns.triggers[0].keyword == "没有数据"
    assert p2.browsing.viewing_strategy.follow == ["tech", "social"]
    assert p2.behavior.reply_probability == 0.55


def test_persona_defaults():
    p = PersonaArchetype(name="test")
    assert p.browsing.pattern == "scheduled"
    assert p.behavior.like_probability == 0.3
    assert p.cognitive.emotional_reactivity == 0.5
