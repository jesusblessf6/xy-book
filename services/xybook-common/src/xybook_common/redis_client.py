from redis.asyncio import Redis

from xybook_common.config import ServiceSettings


def get_redis_pool(url: str) -> Redis:
    return Redis.from_url(url, decode_responses=True)
