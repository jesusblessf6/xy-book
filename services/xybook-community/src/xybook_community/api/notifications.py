from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..models.notification import Notification
from ..schemas.notification import NotificationMarkRead, NotificationRead

router = APIRouter(tags=["notifications"])


@router.get("/notifications", response_model=list[NotificationRead])
async def get_notifications(
    user_id: uuid.UUID = Query(...),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/notifications/read")
async def mark_notifications_read(
    body: NotificationMarkRead,
    user_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        update(Notification)
        .where(
            Notification.id.in_(body.notification_ids),
            Notification.user_id == user_id,
        )
        .values(read=True)
    )
    await db.execute(stmt)
    await db.commit()
    return {"marked": len(body.notification_ids)}
