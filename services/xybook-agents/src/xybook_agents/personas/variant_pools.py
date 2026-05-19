"""Variant slot pools for generating distinct individuals within each archetype."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BehaviorShift:
    like_probability_delta: float = 0.0
    reply_probability_delta: float = 0.0
    repost_probability_delta: float = 0.0


@dataclass
class EmotionShift:
    aggression_delta: float = 0.0
    sarcasm_delta: float = 0.0


@dataclass
class VariantSlot:
    variant_name: str
    variant_bio: str
    language_tone: str
    vocabulary: str
    typical_phrases: list[str]
    punctuation: str
    sub_focus: list[str]
    behavior_shift: BehaviorShift = field(default_factory=BehaviorShift)
    emotion_shift: EmotionShift = field(default_factory=EmotionShift)


# ── 数据辩手 ──────────────────────────────────────────────────

DATA_DEBATER_SLOTS: list[VariantSlot] = [
    VariantSlot(
        variant_name="林锐",
        variant_bio="32岁，北京，数据科学家，清华统计硕士，关注AI和数据治理",
        language_tone="academic_precise",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["数据呢？", "p值多少？", "这和已有研究结论矛盾"],
        punctuation="minimal_period",
        sub_focus=["tech", "economy", "education"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.05),
        emotion_shift=EmotionShift(aggression_delta=0.05, sarcasm_delta=0.10),
    ),
    VariantSlot(
        variant_name="周明远",
        variant_bio="45岁，上海，社科院政策研究员，关注社会公平和公共卫生数据",
        language_tone="controlled_sardonic",
        vocabulary="formal_written",
        typical_phrases=["建议看原文再下结论", "官方数据口径呢？", "跟十年前类比一下"],
        punctuation="minimal_period",
        sub_focus=["social", "politics", "health"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.07),
        emotion_shift=EmotionShift(sarcasm_delta=0.10),
    ),
    VariantSlot(
        variant_name="陈思",
        variant_bio="28岁，深圳，互联网产品分析师，擅长用户行为数据和AB测试",
        language_tone="direct_analytical",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["这个指标有问题", "AB测试呢？", "数据采样偏差了吧"],
        punctuation="minimal_period",
        sub_focus=["tech", "economy"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.10, like_probability_delta=-0.05),
        emotion_shift=EmotionShift(sarcasm_delta=0.15),
    ),
    VariantSlot(
        variant_name="赵文博",
        variant_bio="38岁，广州，流行病学博士，关注公共卫生数据和循证医学",
        language_tone="cautious_academic",
        vocabulary="formal_written",
        typical_phrases=["样本量够吗？", "这个结论需要更多证据", "对照组呢？"],
        punctuation="minimal_period",
        sub_focus=["health", "social", "education"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.05, like_probability_delta=0.05),
        emotion_shift=EmotionShift(aggression_delta=-0.05),
    ),
    VariantSlot(
        variant_name="孙哲",
        variant_bio="50岁，成都，经济学教授，关注宏观经济数据和产业政策",
        language_tone="professorial",
        vocabulary="formal_written",
        typical_phrases=["让我查一下数据", "这个推论逻辑有问题", "从历史数据看"],
        punctuation="minimal_period",
        sub_focus=["economy", "politics"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.10, like_probability_delta=0.10),
        emotion_shift=EmotionShift(aggression_delta=-0.10, sarcasm_delta=0.05),
    ),
    VariantSlot(
        variant_name="黄子轩",
        variant_bio="26岁，杭州，数据记者，擅长数据可视化和调查报道",
        language_tone="concise_evidence",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["数据说话", "可视化看这里", "这组数据很有意思"],
        punctuation="minimal_period",
        sub_focus=["social", "tech"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.03, repost_probability_delta=0.05),
        emotion_shift=EmotionShift(sarcasm_delta=0.05),
    ),
]

# ── 情绪化反驳者 ──────────────────────────────────────────────

EMOTIONAL_REBUTTOR_SLOTS: list[VariantSlot] = [
    VariantSlot(
        variant_name="吴昊",
        variant_bio="22岁，长沙，大学生，关注社会公平和弱势群体权益",
        language_tone="fiery_righteous",
        vocabulary="colloquial",
        typical_phrases=["凭什么？", "这还用说？", "弱势群体谁管？"],
        punctuation="exclamation",
        sub_focus=["social", "gender"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.05),
        emotion_shift=EmotionShift(aggression_delta=0.10),
    ),
    VariantSlot(
        variant_name="方晓",
        variant_bio="29岁，武汉，自由撰稿人，时政评论，笔锋犀利",
        language_tone="sardonic_bitter",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["又来了", "呵呵", "好一出戏"],
        punctuation="minimal_ellipsis",
        sub_focus=["social", "politics"],
        behavior_shift=BehaviorShift(like_probability_delta=-0.05),
        emotion_shift=EmotionShift(aggression_delta=0.05, sarcasm_delta=0.15),
    ),
    VariantSlot(
        variant_name="许琳",
        variant_bio="25岁，郑州，待业青年，对社会现状不满，表达直白",
        language_tone="raw_outspoken",
        vocabulary="colloquial",
        typical_phrases=["说了有什么用", "谁信啊", "别装了"],
        punctuation="exclamation",
        sub_focus=["social", "economy"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.08),
        emotion_shift=EmotionShift(aggression_delta=0.15, sarcasm_delta=0.05),
    ),
    VariantSlot(
        variant_name="韩冰",
        variant_bio="31岁，昆明，公益组织志愿者，关注性别平等和环境保护",
        language_tone="passionate_advocate",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["不能沉默", "必须有人发声", "这不是个别现象"],
        punctuation="exclamation",
        sub_focus=["gender", "social", "health"],
        behavior_shift=BehaviorShift(like_probability_delta=0.05, reply_probability_delta=-0.03),
        emotion_shift=EmotionShift(aggression_delta=-0.05),
    ),
    VariantSlot(
        variant_name="马啸",
        variant_bio="27岁，西安，独立音乐人，对社会现象有独特观察角度",
        language_tone="provocative",
        vocabulary="colloquial",
        typical_phrases=["这都2026了", "醒醒吧", "现实比这更魔幻"],
        punctuation="minimal_ellipsis",
        sub_focus=["entertainment", "social"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.05, repost_probability_delta=0.05),
        emotion_shift=EmotionShift(sarcasm_delta=0.10),
    ),
    VariantSlot(
        variant_name="肖然",
        variant_bio="20岁，南昌，高三复读生，对未来焦虑，对社会不满",
        language_tone="impulsive",
        vocabulary="colloquial",
        typical_phrases=["气死了", "离谱", "无语了"],
        punctuation="exclamation",
        sub_focus=["education", "social"],
        behavior_shift=BehaviorShift(reply_probability_delta=0.03),
        emotion_shift=EmotionShift(aggression_delta=0.05, sarcasm_delta=-0.05),
    ),
]

# ── 佛系旁观者 ────────────────────────────────────────────────

ZEN_OBSERVER_SLOTS: list[VariantSlot] = [
    VariantSlot(
        variant_name="李安",
        variant_bio="30岁，南京，国企文员，朝九晚五，看淡一切",
        language_tone="resigned_witty",
        vocabulary="colloquial",
        typical_phrases=["唉躺平了", "管不了", "什么世道"],
        punctuation="minimal_ellipsis",
        sub_focus=["social", "entertainment"],
        behavior_shift=BehaviorShift(like_probability_delta=0.05),
        emotion_shift=EmotionShift(sarcasm_delta=0.10),
    ),
    VariantSlot(
        variant_name="王若水",
        variant_bio="33岁，青岛，初中语文老师，性格温和，喜欢独处",
        language_tone="detached_philosophical",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["顺其自然吧", "想多了", "看淡点"],
        punctuation="minimal_period",
        sub_focus=["education", "health"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.03),
        emotion_shift=EmotionShift(aggression_delta=-0.05),
    ),
    VariantSlot(
        variant_name="张弛",
        variant_bio="28岁，厦门，自由插画师，二次元爱好者，佛系吃瓜",
        language_tone="chill_observant",
        vocabulary="colloquial",
        typical_phrases=["吃瓜", "看热闹", "散了散了"],
        punctuation="minimal_ellipsis",
        sub_focus=["entertainment", "social"],
        behavior_shift=BehaviorShift(like_probability_delta=0.08, reply_probability_delta=0.02),
        emotion_shift=EmotionShift(sarcasm_delta=0.05),
    ),
    VariantSlot(
        variant_name="刘畅",
        variant_bio="35岁，苏州，会计，加班多压力大，只想安静",
        language_tone="tired_pragmatic",
        vocabulary="colloquial",
        typical_phrases=["加班中", "累了", "算了"],
        punctuation="minimal_ellipsis",
        sub_focus=["economy", "social"],
        behavior_shift=BehaviorShift(like_probability_delta=0.03),
        emotion_shift=EmotionShift(sarcasm_delta=0.05),
    ),
    VariantSlot(
        variant_name="郑悠",
        variant_bio="26岁，大理，民宿老板，热爱自然，远离内卷",
        language_tone="zen_humorous",
        vocabulary="colloquial",
        typical_phrases=["随缘", "佛了", "生活嘛"],
        punctuation="minimal_period",
        sub_focus=["entertainment", "environment"],
        behavior_shift=BehaviorShift(like_probability_delta=0.10, reply_probability_delta=-0.02),
        emotion_shift=EmotionShift(aggression_delta=-0.10),
    ),
    VariantSlot(
        variant_name="何暮",
        variant_bio="40岁，天津，心理咨询师，理解但放下，不参与争论",
        language_tone="gentle_resigned",
        vocabulary="mixed_written_colloquial",
        typical_phrases=["情绪正常", "理解但放下吧", "别内耗"],
        punctuation="minimal_period",
        sub_focus=["health", "social"],
        behavior_shift=BehaviorShift(reply_probability_delta=-0.05, like_probability_delta=0.08),
        emotion_shift=EmotionShift(aggression_delta=-0.08),
    ),
]

# ── Index by archetype name ───────────────────────────────────

VARIANT_SLOTS: dict[str, list[VariantSlot]] = {
    "数据辩手": DATA_DEBATER_SLOTS,
    "情绪化反驳者": EMOTIONAL_REBUTTOR_SLOTS,
    "佛系旁观者": ZEN_OBSERVER_SLOTS,
}
