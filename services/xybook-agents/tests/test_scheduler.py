"""Tests for the AgentScheduler (Redis sorted-set based)."""

import asyncio
from datetime import datetime, timedelta, timezone

import fakeredis.aioredis
import pytest

from xybook_agents.scheduler.agent_scheduler import AgentScheduler


async def _make_scheduler():
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    return AgentScheduler(redis)


def test_schedule_and_get_due():
    async def _run():
        scheduler = await _make_scheduler()
        now = datetime.now(timezone.utc)
        past = now - timedelta(minutes=5)
        future = now + timedelta(minutes=5)

        await scheduler.schedule_next_browse("agent-1", past)
        await scheduler.schedule_next_browse("agent-2", future)

        due = await scheduler.get_due_agent_ids()
        assert "agent-1" in due
        assert "agent-2" not in due

    asyncio.run(_run())


def test_remove_agent():
    async def _run():
        scheduler = await _make_scheduler()
        past = datetime.now(timezone.utc) - timedelta(minutes=1)
        await scheduler.schedule_next_browse("agent-x", past)
        await scheduler.remove_agent("agent-x")

        due = await scheduler.get_due_agent_ids()
        assert "agent-x" not in due

    asyncio.run(_run())


def test_count_pending():
    async def _run():
        scheduler = await _make_scheduler()
        now = datetime.now(timezone.utc)
        assert await scheduler.count_pending() == 0

        await scheduler.schedule_next_browse("a1", now + timedelta(minutes=10))
        await scheduler.schedule_next_browse("a2", now + timedelta(minutes=20))

        assert await scheduler.count_pending() == 2

    asyncio.run(_run())


def test_get_next_schedule_time():
    async def _run():
        scheduler = await _make_scheduler()
        now = datetime.now(timezone.utc)
        result = await scheduler.get_next_schedule_time()
        assert result is None

        await scheduler.schedule_next_browse("a1", now + timedelta(minutes=5))
        await scheduler.schedule_next_browse("a2", now + timedelta(minutes=3))

        result = await scheduler.get_next_schedule_time()
        assert result is not None
        assert result < now.timestamp() + timedelta(minutes=4).total_seconds()

    asyncio.run(_run())


def test_due_ids_removed_after_get():
    async def _run():
        scheduler = await _make_scheduler()
        past = datetime.now(timezone.utc) - timedelta(minutes=1)
        await scheduler.schedule_next_browse("agent-due", past)
        due1 = await scheduler.get_due_agent_ids()
        assert "agent-due" in due1

        due2 = await scheduler.get_due_agent_ids()
        assert len(due2) == 0

    asyncio.run(_run())
