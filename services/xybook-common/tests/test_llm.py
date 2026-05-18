import asyncio

from xybook_common.llm import MockLLMProvider


def test_mock_llm_persona_match():
    llm = MockLLMProvider()
    # Run multiple times since responses are random
    results = set()
    for _ in range(20):
        result = asyncio.run(llm.generate("你是数据辩手，请回复"))
        results.add(result)
    # Should produce at least one 数据辩手-specific reply
    from xybook_common.llm import _REPLIES_BY_TYPE
    expected = set(_REPLIES_BY_TYPE["数据辩手"])
    assert results & expected, f"No matching replies found in {results}"


def test_mock_llm_fallback():
    llm = MockLLMProvider()
    result = asyncio.run(llm.generate("随便说说"))
    assert isinstance(result, str)
    assert len(result) > 0
