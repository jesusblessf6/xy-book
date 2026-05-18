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

_FALLBACK_REPLIES = [
    "有道理。",
    "不太确定，再看看。",
    "嗯，了解了。",
    "值得关注。",
    "先让子弹飞一会。",
]


class MockLLMProvider:
    """Returns placeholder text based on persona type detected in prompt."""

    async def generate(self, prompt: str, **kwargs) -> str:
        for persona_name, replies in _REPLIES_BY_TYPE.items():
            if persona_name in prompt:
                return random.choice(replies)
        return random.choice(_FALLBACK_REPLIES)
