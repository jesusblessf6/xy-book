from functools import lru_cache

from xybook_common.config import ServiceSettings


class PipelineSettings(ServiceSettings):
    service_name: str = "pipeline"
    service_port: int = 8004
    database_url: str = "postgresql+asyncpg://wing@localhost:5432/pipeline"
    redis_url: str = "redis://localhost:6379/0"
    community_url: str = "http://localhost:8001"


@lru_cache
def get_settings() -> PipelineSettings:
    return PipelineSettings()
