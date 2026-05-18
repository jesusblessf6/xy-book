from __future__ import annotations

from datetime import datetime

from redis.asyncio import Redis


class AgentScheduler:
    """Redis Sorted Set based agent browse scheduler."""

    def __init__(self, redis: Redis):
        self.redis = redis
        self.schedule_key = "agent:browse_schedule"

    async def schedule_next_browse(self, agent_id: str, next_time: datetime) -> None:
        await self.redis.zadd(
            self.schedule_key, {agent_id: next_time.timestamp()}
        )

    async def get_due_agent_ids(self) -> list[str]:
        now_ts = datetime.now().timestamp()
        agent_ids = await self.redis.zrangebyscore(self.schedule_key, 0, now_ts)
        if agent_ids:
            await self.redis.zremrangebyscore(self.schedule_key, 0, now_ts)
        return [aid if isinstance(aid, str) else aid.decode() for aid in agent_ids]

    async def get_next_schedule_time(self) -> float | None:
        result = await self.redis.zrange(self.schedule_key, 0, 0, withscores=True)
        if result:
            return result[0][1]
        return None

    async def count_pending(self) -> int:
        return await self.redis.zcard(self.schedule_key)

    async def remove_agent(self, agent_id: str) -> None:
        await self.redis.zrem(self.schedule_key, agent_id)
