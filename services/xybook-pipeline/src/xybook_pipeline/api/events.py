import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from xybook_common.enums import EventStatus

from ..dependencies import get_db
from ..models.event import Event
from ..models.event_post_mapping import EventPostMapping
from ..schemas.event import EventCreate, EventRead, EventUpdate
from ..services.event_renderer import render_post_content

router = APIRouter(tags=["events"])


@router.post("/events", response_model=EventRead, status_code=201)
async def create_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    event = Event(
        post_type=body.post_type,
        source_author=body.source_author,
        source_platform=body.source_platform,
        source_url=body.source_url,
        source_content=body.source_content,
        source_media=body.source_media,
        source_metrics=body.source_metrics,
        direct_content=body.direct_content,
        operator_id=body.operator_id,
        operator_comment=body.operator_comment,
        category=body.category,
        tags=body.tags,
        intensity=body.intensity,
        scheduled_at=body.scheduled_at,
    )
    if body.scheduled_at:
        event.status = EventStatus.SCHEDULED
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.get("/events", response_model=list[EventRead])
async def list_events(
    status_filter: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Event).order_by(Event.created_at.desc()).limit(limit).offset(offset)
    if status_filter:
        stmt = stmt.where(Event.status == status_filter)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/events/{event_id}", response_model=EventRead)
async def get_event(event_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    return event


@router.patch("/events/{event_id}", response_model=EventRead)
async def update_event(
    event_id: uuid.UUID, body: EventUpdate, db: AsyncSession = Depends(get_db)
):
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(event, k, v)
    await db.commit()
    await db.refresh(event)
    return event


@router.post("/events/{event_id}/activate", response_model=EventRead)
async def activate_event(
    event_id: uuid.UUID, request: Request, db: AsyncSession = Depends(get_db)
):
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    if event.status not in (EventStatus.DRAFT, EventStatus.SCHEDULED):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Cannot activate event in status: {event.status}",
        )

    event.status = EventStatus.ACTIVE
    event.activated_at = datetime.now(timezone.utc)

    # Render content and create Post in Community Service
    community = request.app.state.community
    content = render_post_content(event)
    post_data = await community.create_post(
        author_id=event.operator_id,
        content=content,
        category=event.category,
        tags=event.tags,
        post_type=event.post_type,
    )
    post_id = uuid.UUID(post_data["id"])

    # Create EventPostMapping
    mapping = EventPostMapping(event_id=event.id, post_id=post_id)
    db.add(mapping)

    # Set initial event_heat in Redis
    redis = request.app.state.redis
    await redis.set(f"post:{post_id}:event_heat", "1.0")

    await db.commit()
    await db.refresh(event)
    return event
