from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from xybook_common.clients.community_client import CommunityClient
from xybook_common.llm import LLMProvider
from xybook_common.persona import PersonaArchetype

from ..models.agent import Agent
from ..scheduler.agent_scheduler import AgentScheduler
from .content import compose_original_post, compose_reply
from .decisions import (
    compute_delay,
    compute_next_browse_time,
    decide_action,
    filter_by_interest,
    should_check_my_threads,
)

logger = logging.getLogger(__name__)


async def run_browse_session(
    agent: Agent,
    persona: PersonaArchetype,
    community: CommunityClient,
    scheduler: AgentScheduler,
    llm: LLMProvider,
) -> None:
    """Execute one browse session for an agent."""
    logger.info(f"Agent {agent.id} ({persona.name}) starting browse session")

    try:
        # Phase 1: Fetch timeline
        feed = await community.get_feed(
            sort=persona.browsing.viewing_strategy.timeline_sort, limit=50
        )

        # Phase 2: Filter unseen
        read_states = await community.get_read_states(agent.user_id)
        seen_ids = {uuid.UUID(rs["post_id"]) for rs in read_states}
        new_posts = [p for p in feed if uuid.UUID(p["id"]) not in seen_ids]

        # Phase 3: Filter by interest
        filtered = filter_by_interest(persona, new_posts)

        # Phase 4: React to each post
        for post in filtered:
            post_id = uuid.UUID(post["id"])

            # Mark as seen
            try:
                await community.record_read_state(agent.user_id, post_id)
            except Exception:
                pass

            # Decide action
            action = decide_action(persona, post)

            if action == "silent":
                continue

            # Simulate thinking delay (capped for development)
            delay = min(compute_delay(persona, action, post), 5.0)
            await asyncio.sleep(delay)

            try:
                if action == "like":
                    await community.like_post(post_id, agent.user_id)
                    logger.info(f"Agent {agent.id} liked post {post_id}")

                elif action == "reply":
                    content = await compose_reply(persona, post, llm)
                    root_post_id = uuid.UUID(post.get("root_post_id", post["id"]))
                    await community.create_post(
                        author_id=agent.user_id,
                        content=content,
                        parent_id=post_id,
                        root_post_id=root_post_id,
                        category=post.get("category"),
                    )
                    agent.last_posted_at = datetime.now(timezone.utc)
                    logger.info(f"Agent {agent.id} replied to post {post_id}")

                elif action == "repost":
                    await community.repost(post_id, agent.user_id)
                    logger.info(f"Agent {agent.id} reposted post {post_id}")

            except Exception as e:
                logger.error(f"Agent {agent.id} action {action} failed: {e}")

        # Phase 5: Check my threads
        if should_check_my_threads(persona):
            try:
                my_threads = await community.get_my_threads(agent.user_id)
                for thread in my_threads[:5]:  # Limit to 5 threads
                    thread_id = uuid.UUID(thread["id"])
                    since = agent.last_browsed_at or datetime.min.replace(tzinfo=timezone.utc)
                    new_replies = await community.get_new_replies(thread_id, since)
                    for reply in new_replies[:3]:
                        action = decide_action(persona, reply)
                        if action == "like":
                            try:
                                await community.like_post(uuid.UUID(reply["id"]), agent.user_id)
                            except Exception:
                                pass
                        elif action == "reply":
                            try:
                                content = await compose_reply(persona, reply, llm)
                                await community.create_post(
                                    author_id=agent.user_id,
                                    content=content,
                                    parent_id=uuid.UUID(reply["id"]),
                                    root_post_id=uuid.UUID(reply.get("root_post_id", reply["id"])),
                                )
                            except Exception:
                                pass
            except Exception as e:
                logger.error(f"Agent {agent.id} thread check failed: {e}")

    except Exception as e:
        logger.error(f"Agent {agent.id} browse session failed: {e}")

    # Update state
    agent.last_browsed_at = datetime.now(timezone.utc)

    # Schedule next browse
    next_time = compute_next_browse_time(persona)
    agent.next_browse_at = next_time
    await scheduler.schedule_next_browse(str(agent.id), next_time)

    logger.info(f"Agent {agent.id} next browse at {next_time}")
