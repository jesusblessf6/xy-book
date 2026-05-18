from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..models.read_state import ReadState
from ..schemas.read_state import ReadStateCreate, ReadStateRead

router = APIRouter(tags=["read-states"])


@router.post("/read-states", response_model=ReadStateRead, status_code=201)
async def record_read_state(body: ReadStateCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    existing = await db.execute(
        select(ReadState).where(
            ReadState.agent_id == body.agent_id, ReadState.post_id == body.post_id
        )
    )
    state = existing.scalar_one_or_none()
    if state:
        state.last_checked_at = now
        await db.commit()
        await db.refresh(state)
        return state

    state = ReadState(
        agent_id=body.agent_id,
        post_id=body.post_id,
        seen_at=now,
        last_checked_at=now,
    )
    db.add(state)
    await db.commit()
    await db.refresh(state)
    return state


@router.get("/read-states", response_model=list[ReadStateRead])
async def list_read_states(
    agent_id: uuid.UUID = Query(...),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(ReadState)
        .where(ReadState.agent_id == agent_id)
        .order_by(ReadState.seen_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


class BatchReadStateRequest(BaseModel):
    agent_id: uuid.UUID
    post_ids: list[uuid.UUID]


@router.post("/read-states/batch", response_model=list[ReadStateRead])
async def batch_read_states(
    body: BatchReadStateRequest, db: AsyncSession = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    results = []

    for post_id in body.post_ids:
        existing = await db.execute(
            select(ReadState).where(
                ReadState.agent_id == body.agent_id, ReadState.post_id == post_id
            )
        )
        state = existing.scalar_one_or_none()
        if state:
            state.last_checked_at = now
        else:
            state = ReadState(
                agent_id=body.agent_id,
                post_id=post_id,
                seen_at=now,
                last_checked_at=now,
            )
            db.add(state)
        results.append(state)

    await db.commit()
    for s in results:
        await db.refresh(s)
    return results
