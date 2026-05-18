"""Render Event data into Post content for Community Service."""

from __future__ import annotations

from ..models.event import Event


def render_post_content(event: Event) -> str:
    """Render an Event into content suitable for a Community Post."""
    parts: list[str] = []

    if event.post_type == "repost" and event.source_content:
        # Repost: quote the original source
        source_header = f"转载自 @{event.source_author or '未知'} ({event.source_platform or '未知平台'}):"
        parts.append(source_header)
        parts.append(f"> {event.source_content}")
        if event.operator_comment:
            parts.append("")
            parts.append(event.operator_comment)

    elif event.post_type == "original" and event.direct_content:
        parts.append(event.direct_content)

    else:
        # Mixed or fallback: combine both
        if event.source_content:
            source_header = f"转载自 @{event.source_author or '未知'} ({event.source_platform or '未知平台'}):"
            parts.append(source_header)
            parts.append(f"> {event.source_content}")
        if event.direct_content:
            if parts:
                parts.append("")
            parts.append(event.direct_content)
        if event.operator_comment:
            if parts:
                parts.append("")
            parts.append(event.operator_comment)

    return "\n".join(parts) if parts else "（空内容）"
