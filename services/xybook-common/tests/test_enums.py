from xybook_common.enums import (
    EventIntensity,
    EventStatus,
    EmotionType,
    InteractionType,
    NotificationType,
    PostCategory,
    PostStatus,
    PostType,
    INTENSITY_HALF_LIFE,
)


def test_post_category_values():
    assert PostCategory.SOCIAL == "social"
    assert PostCategory.TECH == "tech"
    assert PostCategory.GENDER == "gender"
    assert len(PostCategory) == 10


def test_event_intensity_half_life():
    assert INTENSITY_HALF_LIFE[EventIntensity.LOW] == 12
    assert INTENSITY_HALF_LIFE[EventIntensity.MEDIUM] == 24
    assert INTENSITY_HALF_LIFE[EventIntensity.HIGH] == 48
    assert INTENSITY_HALF_LIFE[EventIntensity.EXTREME] == 72


def test_post_status_values():
    assert PostStatus.PUBLISHED == "published"
    assert PostStatus.DELETED == "deleted"
    assert PostStatus.HIDDEN == "hidden"


def test_event_status_values():
    assert EventStatus.DRAFT == "draft"
    assert EventStatus.ACTIVE == "active"
    assert EventStatus.EXPIRED == "expired"


def test_emotion_type_values():
    assert EmotionType.ANGER == "anger"
    assert EmotionType.SADNESS == "sadness"
    assert EmotionType.NEUTRAL == "neutral"


def test_interaction_type_values():
    assert InteractionType.LIKE == "like"
    assert InteractionType.REPLY == "reply"
    assert InteractionType.REPOST == "repost"


def test_notification_type_values():
    assert NotificationType.LIKE == "like"
    assert NotificationType.FOLLOW == "follow"
    assert NotificationType.REPLY == "reply"
