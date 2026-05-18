from functools import lru_cache

from xybook_common.config import ServiceSettings


class CommunitySettings(ServiceSettings):
    service_name: str = "community"
    service_port: int = 8001
    database_url: str = "postgresql+asyncpg://wing@localhost:5432/community"


@lru_cache
def get_settings() -> CommunitySettings:
    return CommunitySettings()
