import asyncio

from xybook_common.llm import MockLLMProvider


def test_mock_llm_persona_match():
    llm = MockLLMProvider()
    results = set()
    for _ in range(20):
        result = asyncio.run(llm.generate("你是数据辩手，请回复"))
        results.add(result)
    from xybook_common.llm import _REPLIES_BY_TYPE
    expected = set(_REPLIES_BY_TYPE["数据辩手"])
    assert results & expected, f"No matching replies found in {results}"


def test_mock_llm_variant_match():
    llm = MockLLMProvider()
    results = set()
    for _ in range(20):
        result = asyncio.run(llm.generate("你是林锐（数据辩手型），32岁"))
        results.add(result)
    from xybook_common.llm import _VARIANT_REPLIES
    expected = set(_VARIANT_REPLIES["林锐"])
    assert results & expected, f"No variant replies found in {results}"


def test_mock_llm_variant_takes_priority():
    llm = MockLLMProvider()
    # Prompt contains both variant name "林锐" and archetype "数据辩手"
    # Variant should take priority
    results = set()
    for _ in range(20):
        result = asyncio.run(llm.generate("你是林锐（数据辩手型），请回复"))
        results.add(result)
    from xybook_common.llm import _VARIANT_REPLIES
    variant_expected = set(_VARIANT_REPLIES["林锐"])
    # Should produce at least one variant-specific reply
    assert results & variant_expected, f"Variant replies not prioritized in {results}"


def test_mock_llm_fallback():
    llm = MockLLMProvider()
    result = asyncio.run(llm.generate("随便说说"))
    assert isinstance(result, str)
    assert len(result) > 0
