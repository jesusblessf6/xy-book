from enum import StrEnum


class PostCategory(StrEnum):
    SOCIAL = "social"
    TECH = "tech"
    GENDER = "gender"
    POLITICS = "politics"
    ECONOMY = "economy"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    ENVIRONMENT = "environment"
    OTHER = "other"


class PostType(StrEnum):
    REPOST = "repost"
    ORIGINAL = "original"
    MIXED = "mixed"


class PostStatus(StrEnum):
    PUBLISHED = "published"
    DELETED = "deleted"
    HIDDEN = "hidden"


class EmotionType(StrEnum):
    ANGER = "anger"
    SADNESS = "sadness"
    ANXIETY = "anxiety"
    AMUSEMENT = "amusement"
    CONTEMPT = "contempt"
    EMPATHY = "empathy"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"


class NotificationType(StrEnum):
    REPLY = "reply"
    LIKE = "like"
    FOLLOW = "follow"
    REPOST = "repost"
    MENTION = "mention"


class EventStatus(StrEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    EXPIRED = "expired"
    ARCHIVED = "archived"


class EventIntensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class InteractionType(StrEnum):
    LIKE = "like"
    REPLY = "reply"
    REPOST = "repost"


# intensity → half-life hours mapping (见 EVENT_ENGINE.md)
INTENSITY_HALF_LIFE: dict[EventIntensity, int] = {
    EventIntensity.LOW: 12,
    EventIntensity.MEDIUM: 24,
    EventIntensity.HIGH: 48,
    EventIntensity.EXTREME: 72,
}
