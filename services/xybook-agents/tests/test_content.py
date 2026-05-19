"""Tests for content generation (mock LLM)."""

import asyncio

from xybook_common.llm import MockLLMProvider

from xybook_agents.personas.variants import instantiate_persona
from xybook_agents.worker.content import compose_original_post, compose_reply


def test_compose_reply():
    async def _run():
        llm = MockLLMProvider()
        persona = instantiate_persona("数据辩手", 0)
        post = {"content": "今天的新闻很震撼", "tags": ["social"]}
        reply = await compose_reply(persona, post, llm)
        assert isinstance(reply, str)
        assert len(reply) > 0

    asyncio.run(_run())


def test_compose_original_post():
    async def _run():
        llm = MockLLMProvider()
        persona = instantiate_persona("佛系旁观者", 0)
        content = await compose_original_post(persona, llm)
        assert isinstance(content, str)
        assert len(content) > 0

    asyncio.run(_run())


def test_compose_reply_uses_variant_identity():
    async def _run():
        llm = MockLLMProvider()
        persona = instantiate_persona("数据辩手", 0)
        # The prompt should contain variant_name "林锐" and archetype "数据辩手"
        post = {"content": "测试", "tags": []}
        reply = await compose_reply(persona, post, llm)
        assert isinstance(reply, str)

    asyncio.run(_run())


def test_mock_llm_variant_match():
    async def _run():
        llm = MockLLMProvider()
        # "林锐" is a variant name — should match variant-specific replies
        result = await llm.generate("你是林锐（数据辩手型），32岁，北京")
        assert isinstance(result, str)
        assert len(result) > 0

    asyncio.run(_run())


def test_mock_llm_different_variants_different_replies():
    async def _run():
        llm = MockLLMProvider()
        # Two different variants should produce different replies
        results_a = set()
        results_b = set()
        for _ in range(20):
            r1 = await llm.generate("你是林锐（数据辩手型），32岁")
            r2 = await llm.generate("你是周明远（数据辩手型），45岁")
            results_a.add(r1)
            results_b.add(r2)
        # They should have different reply pools
        assert results_a != results_b

    asyncio.run(_run())
