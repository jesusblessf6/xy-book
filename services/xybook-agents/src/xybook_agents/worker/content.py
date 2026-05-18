from __future__ import annotations

from xybook_common.llm import LLMProvider
from xybook_common.persona import PersonaArchetype


async def compose_reply(
    persona: PersonaArchetype, post: dict, llm: LLMProvider
) -> str:
    """Generate a reply to a post using the LLM provider."""
    phrases = "、".join(persona.language_style.typical_phrases[:3])
    prompt = (
        f"你是{persona.name}，{persona.demographics}。\n"
        f"你的性格：{'、'.join(persona.core_traits)}\n"
        f"你说话的风格：{persona.language_style.tone}，常用语：{phrases}\n\n"
        f"帖子内容：{post.get('content', '')}\n"
        f"话题标签：{post.get('tags', [])}\n\n"
        f"请以你的身份和风格，对上述帖子发表评论。保持人设一致，不要说'作为一个AI'。"
    )
    return await llm.generate(prompt)


async def compose_original_post(
    persona: PersonaArchetype, llm: LLMProvider
) -> str:
    """Generate an original post from the agent."""
    phrases = "、".join(persona.language_style.typical_phrases[:3])
    prompt = (
        f"你是{persona.name}，{persona.demographics}。\n"
        f"你的性格：{'、'.join(persona.core_traits)}\n"
        f"你说话的风格：{persona.language_style.tone}，常用语：{phrases}\n\n"
        f"你想发一条帖子，表达自己的观点或感受。"
        f"像真人发朋友圈/微博那样，不要太长。"
    )
    return await llm.generate(prompt)
