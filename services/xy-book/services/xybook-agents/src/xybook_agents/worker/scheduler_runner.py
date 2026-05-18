from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from xybook_common.clients.community_client import CommunityClient
from xybook_common.llm import LLMProvider
from xybook_common.persona import PersonaArchetype

from ..models.agent import Agent
from ..scheduler.agent_scheduler import AgentScheduler
from .agent_loop import run_browse_session

logger = logging.getLogger(__name__)


async def run_scheduler(
    scheduler: AgentScheduler,
    session_factory: async_sessionmaker[AsyncSession],
    community: CommunityClient,
    llm: LLMProvider,
) -> None:
    """Main scheduler loop: poll for due agents and dispatch browse sessions."""
    logger.info("Scheduler runner started")

    while True:
        try:
            due_agent_ids = await scheduler.get_due_agents()

            if due_agent_ids:
                async with session_factory() as db:
                    for agent_id in due_agent_ids:
                        stmt = select(Agent).where(Agent.id == agent_id)
                        result = await db.execute(stmt)
                        agent = result.scalar_one_or_none()

                        if not agent or agent.status != "active":
                            continue

                        persona = PersonaArchetype.from_dict(agent.persona_config)
                        try:
                            await run_browse_session(
                                agent, persona, community, scheduler, llm
                            )
                            # Persist updated state
                            db.add(agent)
                            await db.commit()
                        except Exception as e:
                            logger.error(f"Agent {agent_id} session error: {e}")
                            await db.rollback()

            # Wait until next due agent or max 5 seconds
            next_score = await scheduler.get_next_schedule_time()
            if next_score:
                wait = max(0, next_score - time.time())
                await asyncio.sleep(min(wait, 5.0))
            else:
                await asyncio.sleep(5.0)

        except asyncio.CancelledError:
            logger.info("Scheduler runner cancelled")
            return
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(5.0)
