from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from xybook_common.exceptions import NotFoundError

from ..models.agent import Agent
from ..personas.templates import ARCHETYPES
from ..personas.variants import generate_username, instantiate_persona
from ..scheduler.agent_scheduler import AgentScheduler
from ..schemas.agent import AgentCreate, AgentRead, BatchCreateRequest
from ..worker.decisions import compute_next_browse_time

api_router = APIRouter(prefix="/api/agents")


def _get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_factory


async def get_db(request: Request) -> AsyncSession:
    factory = _get_session_factory(request)
    async with factory() as session:
        yield session


def _extract_city(bio: str) -> str | None:
    """Extract city name from variant bio like '32岁，北京，数据科学家'."""
    parts = bio.split("，")
    if len(parts) >= 2:
        return parts[1].strip()
    return None


@api_router.get("/", response_model=list[AgentRead], tags=["agents"])
async def list_agents(
    request: Request,
    limit: int = 50,
    offset: int = 0,
):
    factory = _get_session_factory(request)
    async with factory() as db:
        stmt = select(Agent).order_by(Agent.created_at.desc()).limit(limit).offset(offset)
        result = await db.execute(stmt)
        return list(result.scalars().all())


@api_router.post("/", response_model=AgentRead, status_code=201, tags=["agents"])
async def create_agent(body: AgentCreate, request: Request):
    if body.persona_archetype not in ARCHETYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Unknown archetype: {body.persona_archetype}. Choose from: {list(ARCHETYPES.keys())}",
        )

    community = request.app.state.community
    factory = _get_session_factory(request)

    # Create persona variant (need variant_id first)
    async with factory() as db:
        stmt = select(Agent).where(Agent.persona_archetype == body.persona_archetype)
        result = await db.execute(stmt)
        variant_id = len(list(result.scalars().all()))

    persona = instantiate_persona(body.persona_archetype, variant_id)

    # Create user in Community Service
    archetype = ARCHETYPES[body.persona_archetype]
    username = body.username or generate_username(persona.variant_name, body.persona_archetype)
    bio = body.bio or persona.variant_bio or archetype.demographics
    location = _extract_city(persona.variant_bio) if persona.variant_bio else None

    user_data = await community.create_user(
        username=username,
        bio=bio,
        location=location,
        tags=[archetype.name],
        is_agent=True,
    )
    user_id = uuid.UUID(user_data["id"])

    # Save agent
    async with factory() as db:
        agent = Agent(
            user_id=user_id,
            persona_archetype=body.persona_archetype,
            persona_variant=variant_id,
            status="idle",
            persona_config=persona.to_dict(),
        )
        db.add(agent)
        await db.commit()
        await db.refresh(agent)
        return agent


@api_router.post("/batch-create", response_model=list[AgentRead], tags=["agents"])
async def batch_create_agents(body: BatchCreateRequest, request: Request):
    if body.persona_archetype not in ARCHETYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Unknown archetype: {body.persona_archetype}. Choose from: {list(ARCHETYPES.keys())}",
        )

    results = []
    for i in range(body.count):
        create_body = AgentCreate(
            persona_archetype=body.persona_archetype,
        )
        agent = await create_agent(create_body, request)
        results.append(agent)

    return results


@api_router.get("/{agent_id}", response_model=AgentRead, tags=["agents"])
async def get_agent(agent_id: uuid.UUID, request: Request):
    factory = _get_session_factory(request)
    async with factory() as db:
        agent = await db.get(Agent, agent_id)
        if not agent:
            raise NotFoundError("Agent not found")
        return agent


@api_router.post("/{agent_id}/start", response_model=AgentRead, tags=["agents"])
async def start_agent(agent_id: uuid.UUID, request: Request):
    scheduler: AgentScheduler = request.app.state.scheduler
    factory = _get_session_factory(request)

    async with factory() as db:
        agent = await db.get(Agent, agent_id)
        if not agent:
            raise NotFoundError("Agent not found")

        agent.status = "active"

        # Schedule first browse
        from xybook_common.persona import PersonaArchetype
        persona = PersonaArchetype.from_dict(agent.persona_config)
        next_time = compute_next_browse_time(persona)
        agent.next_browse_at = next_time
        await scheduler.schedule_next_browse(str(agent.id), next_time)

        await db.commit()
        await db.refresh(agent)
        return agent


@api_router.post("/{agent_id}/stop", response_model=AgentRead, tags=["agents"])
async def stop_agent(agent_id: uuid.UUID, request: Request):
    scheduler: AgentScheduler = request.app.state.scheduler
    factory = _get_session_factory(request)

    async with factory() as db:
        agent = await db.get(Agent, agent_id)
        if not agent:
            raise NotFoundError("Agent not found")

        agent.status = "paused"
        await scheduler.remove_agent(str(agent.id))

        await db.commit()
        await db.refresh(agent)
        return agent
