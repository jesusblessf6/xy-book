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


def test_mock_llm_persona_specific():
    """MockLLMProvider should return different responses for different personas."""
    async def _run():
        llm = MockLLMProvider()
        p1 = instantiate_persona("数据辩手", 0)
        p2 = instantiate_persona("佛系旁观者", 0)
        r1 = await compose_reply(p1, {"content": "test"}, llm)
        r2 = await compose_reply(p2, {"content": "test"}, llm)
        # Different personas should produce different mock responses
        assert r1 != r2

    asyncio.run(_run())
