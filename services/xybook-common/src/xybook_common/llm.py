from __future__ import annotations

import random
from typing import Protocol


class LLMProvider(Protocol):
    async def generate(self, prompt: str, **kwargs) -> str: ...


_REPLIES_BY_TYPE = {
    "数据辩手": [
        "这个数据需要核实。来源是什么？",
        "先问是不是再问为什么，官方通报呢？",
        "这和已有研究结论矛盾，具体数据在哪？",
        "建议看原文再下结论，标题党太多了。",
        "没有上下文不好判断，等更多信息吧。",
    ],
    "情绪化反驳者": [
        "又来了，这还用说？",
        "背后肯定有人，想都不用想。",
        "呵呵，官方通报你信？",
        "说再多有什么用，该怎样还是怎样。",
        "这都能洗？底线呢？",
    ],
    "佛系旁观者": [
        "唉，躺平了，管不了。",
        "坐等后续吧。",
        "看热闹就好，别太认真。",
        "什么世道……",
        "吃瓜，不发表意见。",
    ],
}

_VARIANT_REPLIES = {
    "林锐": ["p值多少？数据显著性呢？", "这个采样偏差太大了。"],
    "周明远": ["官方数据口径呢？跟十年前类比一下。", "建议看原文再下结论。"],
    "陈思": ["AB测试跑过了吗？", "这个指标有明显问题。"],
    "赵文博": ["样本量够吗？对照组呢？", "这个结论需要更多证据。"],
    "孙哲": ["从历史数据看，这个推论有问题。", "让我查一下数据再回复。"],
    "黄子轩": ["数据说话，可视化看这里。", "这组数据很有意思。"],
    "吴昊": ["凭什么？弱势群体谁管？", "这还用说？"],
    "方晓": ["好一出戏。", "又来了。"],
    "许琳": ["谁信啊？别装了。", "说了有什么用。"],
    "韩冰": ["不能沉默，必须有人发声。", "这不是个别现象。"],
    "马啸": ["醒醒吧，现实比这更魔幻。", "这都2026了。"],
    "肖然": ["离谱！无语了！", "气死了。"],
    "李安": ["唉躺平了，管不了。", "什么世道。"],
    "王若水": ["顺其自然吧。", "想多了。"],
    "张弛": ["吃瓜吃瓜。", "散了散了。"],
    "刘畅": ["累了，算了。", "加班中。"],
    "郑悠": ["随缘吧。", "佛了。"],
    "何暮": ["别内耗，理解但放下吧。", "情绪正常。"],
}

_FALLBACK_REPLIES = [
    "有道理。",
    "不太确定，再看看。",
    "嗯，了解了。",
    "值得关注。",
    "先让子弹飞一会。",
]


class MockLLMProvider:
    """Returns placeholder text based on persona variant or archetype detected in prompt."""

    async def generate(self, prompt: str, **kwargs) -> str:
        # Try variant name first (more specific)
        for variant_name, replies in _VARIANT_REPLIES.items():
            if variant_name in prompt:
                return random.choice(replies)
        # Fall back to archetype name
        for persona_name, replies in _REPLIES_BY_TYPE.items():
            if persona_name in prompt:
                return random.choice(replies)
        return random.choice(_FALLBACK_REPLIES)
