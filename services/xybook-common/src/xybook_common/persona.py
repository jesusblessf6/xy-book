from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmotionTrigger:
    keyword: str
    emotion: str
    intensity_increment: float


@dataclass
class EmotionPatterns:
    primary: str = "neutral"
    triggers: list[EmotionTrigger] = field(default_factory=list)
    intensity: str = "low"
    aggression: float = 0.0
    sarcasm: float = 0.0


@dataclass
class CognitiveConfig:
    emotional_reactivity: float = 0.5
    anti_conformity: float = 0.3
    confrontation_style: str = "withdraw"  # withdraw/escalate/redirect/data_driven/counterattack


@dataclass
class ViewingStrategy:
    timeline_sort: str = "latest"  # latest/hot/following
    scroll_behavior: str = "thorough"  # skim/selective/thorough
    follow: list[str] = field(default_factory=list)  # category enums
    ignore: list[str] = field(default_factory=list)  # category enums
    comment_sort: str = "latest"  # latest/controversial


@dataclass
class BrowsingNotifications:
    enabled: bool = True
    notify_response: str = "batch"  # immediate/batch/ignore


@dataclass
class BrowsingConfig:
    pattern: str = "scheduled"  # frequent/scheduled/searcher/random/lurker
    session_frequency: int = 4  # sessions per day
    peak_hours: list[int] = field(default_factory=lambda: [9, 13, 21])
    avg_response_delay_minutes: int = 30
    viewing_strategy: ViewingStrategy = field(default_factory=ViewingStrategy)
    notifications: BrowsingNotifications = field(default_factory=BrowsingNotifications)


@dataclass
class BehaviorConfig:
    like_probability: float = 0.3
    reply_probability: float = 0.3
    repost_probability: float = 0.15
    activity_level: str = "medium"  # low/medium/high
    max_thread_depth: int = 5
    thread_tracking_tendency: float = 0.5
    avg_reply_length: str = "medium"  # short/medium/long


@dataclass
class SilencePatterns:
    base_silence_ratio: float = 0.4
    topic_mismatch_multiplier: float = 2.5
    topic_match_multiplier: float = 0.4
    fatigue_multiplier: float = 1.5


@dataclass
class LanguageStyle:
    tone: str = "neutral"
    vocabulary: str = "colloquial"
    typical_phrases: list[str] = field(default_factory=list)
    punctuation: str = "minimal"


@dataclass
class PersonaArchetype:
    name: str
    core_traits: list[str] = field(default_factory=list)
    demographics: str = ""
    language_style: LanguageStyle = field(default_factory=LanguageStyle)
    cognitive: CognitiveConfig = field(default_factory=CognitiveConfig)
    emotion_patterns: EmotionPatterns = field(default_factory=EmotionPatterns)
    browsing: BrowsingConfig = field(default_factory=BrowsingConfig)
    behavior: BehaviorConfig = field(default_factory=BehaviorConfig)
    silence_patterns: SilencePatterns = field(default_factory=SilencePatterns)
    variant_name: str = ""
    variant_bio: str = ""

    def to_dict(self) -> dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PersonaArchetype:
        ls = data.get("language_style", {})
        cog = data.get("cognitive", {})
        ep = data.get("emotion_patterns", {})
        br = data.get("browsing", {})
        beh = data.get("behavior", {})
        sp = data.get("silence_patterns", {})

        triggers = [
            EmotionTrigger(**t) for t in ep.get("triggers", [])
        ]

        vs = br.get("viewing_strategy", {})
        bn = br.get("notifications", {})

        return cls(
            name=data["name"],
            core_traits=data.get("core_traits", []),
            demographics=data.get("demographics", ""),
            language_style=LanguageStyle(**ls),
            cognitive=CognitiveConfig(**cog),
            emotion_patterns=EmotionPatterns(
                primary=ep.get("primary", "neutral"),
                triggers=triggers,
                intensity=ep.get("intensity", "low"),
                aggression=ep.get("aggression", 0.0),
                sarcasm=ep.get("sarcasm", 0.0),
            ),
            browsing=BrowsingConfig(
                pattern=br.get("pattern", "scheduled"),
                session_frequency=br.get("session_frequency", 4),
                peak_hours=br.get("peak_hours", [9, 13, 21]),
                avg_response_delay_minutes=br.get("avg_response_delay_minutes", 30),
                viewing_strategy=ViewingStrategy(**vs),
                notifications=BrowsingNotifications(**bn),
            ),
            behavior=BehaviorConfig(**beh),
            silence_patterns=SilencePatterns(**sp),
            variant_name=data.get("variant_name", ""),
            variant_bio=data.get("variant_bio", ""),
        )
