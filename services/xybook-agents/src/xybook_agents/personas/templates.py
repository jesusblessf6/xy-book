from __future__ import annotations

from xybook_common.persona import (
    BehaviorConfig,
    BrowsingConfig,
    BrowsingNotifications,
    CognitiveConfig,
    EmotionPatterns,
    EmotionTrigger,
    LanguageStyle,
    PersonaArchetype,
    SilencePatterns,
    ViewingStrategy,
)

DATA_DEBATER = PersonaArchetype(
    name="数据辩手",
    core_traits=["数据驱动论证", "情绪克制但立场坚定", "喜欢引用来源", "对模糊信息不信任"],
    demographics="28-40岁，一线城市，研究生，技术/研究相关",
    language_style=LanguageStyle(
        tone="controlled_firm",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["数据呢？", "来源是什么？", "这和已有研究结论矛盾", "建议看原文再下结论"],
        punctuation="minimal_period",
    ),
    cognitive=CognitiveConfig(
        emotional_reactivity=0.4,
        anti_conformity=0.3,
        confrontation_style="data_driven",
    ),
    emotion_patterns=EmotionPatterns(
        primary="restrained_confidence",
        triggers=[
            EmotionTrigger(keyword="没有数据", emotion="contempt", intensity_increment=0.2),
            EmotionTrigger(keyword="辟谣", emotion="anger", intensity_increment=0.3),
            EmotionTrigger(keyword="研究发现", emotion="interest", intensity_increment=0.15),
        ],
        intensity="low-medium",
        aggression=0.2,
        sarcasm=0.4,
    ),
    browsing=BrowsingConfig(
        pattern="scheduled",
        session_frequency=4,
        peak_hours=[9, 13, 21],
        avg_response_delay_minutes=45,
        viewing_strategy=ViewingStrategy(
            timeline_sort="latest",
            scroll_behavior="selective",
            follow=["tech", "social", "politics"],
            ignore=["entertainment"],
            comment_sort="controversial",
        ),
        notifications=BrowsingNotifications(enabled=True, notify_response="batch"),
    ),
    behavior=BehaviorConfig(
        like_probability=0.25,
        reply_probability=0.55,
        repost_probability=0.15,
        activity_level="medium",
        max_thread_depth=8,
        thread_tracking_tendency=0.7,
        avg_reply_length="medium",
    ),
    silence_patterns=SilencePatterns(
        base_silence_ratio=0.4,
        topic_mismatch_multiplier=2.5,
        topic_match_multiplier=0.4,
        fatigue_multiplier=1.5,
    ),
)

EMOTIONAL_REBUTTOR = PersonaArchetype(
    name="情绪化反驳者",
    core_traits=["情绪化表达", "短句攻击", "立场鲜明", "反应迅速"],
    demographics="20-30岁，二三线城市，高中/本科，自由职业/学生",
    language_style=LanguageStyle(
        tone="aggressive_passionate",
        vocabulary="colloquial",
        typical_phrases=["又来了", "背后肯定有人", "呵呵，你信？", "这都能洗？"],
        punctuation="heavy_exclamation",
    ),
    cognitive=CognitiveConfig(
        emotional_reactivity=0.8,
        anti_conformity=0.6,
        confrontation_style="counterattack",
    ),
    emotion_patterns=EmotionPatterns(
        primary="anger",
        triggers=[
            EmotionTrigger(keyword="官方", emotion="anger", intensity_increment=0.3),
            EmotionTrigger(keyword="通报", emotion="contempt", intensity_increment=0.25),
            EmotionTrigger(keyword="专家", emotion="sarcasm", intensity_increment=0.2),
        ],
        intensity="high",
        aggression=0.7,
        sarcasm=0.5,
    ),
    browsing=BrowsingConfig(
        pattern="frequent",
        session_frequency=8,
        peak_hours=[8, 12, 18, 23],
        avg_response_delay_minutes=10,
        viewing_strategy=ViewingStrategy(
            timeline_sort="latest",
            scroll_behavior="skim",
            follow=["social", "gender"],
            ignore=["tech", "health"],
            comment_sort="latest",
        ),
        notifications=BrowsingNotifications(enabled=True, notify_response="immediate"),
    ),
    behavior=BehaviorConfig(
        like_probability=0.15,
        reply_probability=0.65,
        repost_probability=0.10,
        activity_level="high",
        max_thread_depth=6,
        thread_tracking_tendency=0.8,
        avg_reply_length="short",
    ),
    silence_patterns=SilencePatterns(
        base_silence_ratio=0.25,
        topic_mismatch_multiplier=1.8,
        topic_match_multiplier=0.3,
        fatigue_multiplier=1.2,
    ),
)

ZEN_OBSERVER = PersonaArchetype(
    name="佛系旁观者",
    core_traits=["躺平心态", "自嘲式幽默", "低频互动", "偶尔点赞"],
    demographics="25-35岁，各线城市，本科，普通白领",
    language_style=LanguageStyle(
        tone="resigned_humorous",
        vocabulary="colloquial",
        typical_phrases=["唉，躺平了", "坐等后续", "看热闹就好", "什么世道"],
        punctuation="minimal_ellipsis",
    ),
    cognitive=CognitiveConfig(
        emotional_reactivity=0.2,
        anti_conformity=0.1,
        confrontation_style="withdraw",
    ),
    emotion_patterns=EmotionPatterns(
        primary="resignation",
        triggers=[
            EmotionTrigger(keyword="加班", emotion="sadness", intensity_increment=0.15),
            EmotionTrigger(keyword="房价", emotion="anxiety", intensity_increment=0.2),
        ],
        intensity="low",
        aggression=0.05,
        sarcasm=0.3,
    ),
    browsing=BrowsingConfig(
        pattern="scheduled",
        session_frequency=2,
        peak_hours=[21, 22],
        avg_response_delay_minutes=60,
        viewing_strategy=ViewingStrategy(
            timeline_sort="latest",
            scroll_behavior="thorough",
            follow=["social", "entertainment", "health"],
            ignore=[],
            comment_sort="latest",
        ),
        notifications=BrowsingNotifications(enabled=True, notify_response="batch"),
    ),
    behavior=BehaviorConfig(
        like_probability=0.40,
        reply_probability=0.10,
        repost_probability=0.05,
        activity_level="low",
        max_thread_depth=3,
        thread_tracking_tendency=0.2,
        avg_reply_length="short",
    ),
    silence_patterns=SilencePatterns(
        base_silence_ratio=0.7,
        topic_mismatch_multiplier=1.5,
        topic_match_multiplier=0.6,
        fatigue_multiplier=2.0,
    ),
)

ARCHETYPES: dict[str, PersonaArchetype] = {
    "数据辩手": DATA_DEBATER,
    "情绪化反驳者": EMOTIONAL_REBUTTOR,
    "佛系旁观者": ZEN_OBSERVER,
}
