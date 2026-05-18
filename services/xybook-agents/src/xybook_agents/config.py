from functools import lru_cache

from xybook_common.config import ServiceSettings


class AgentSettings(ServiceSettings):
    service_name: str = "agents"
    service_port: int = 8002
    community_url: str = "http://localhost:8001"
    database_url: str = "postgresql+asyncpg://wing@localhost:5432/agents"


@lru_cache
def get_settings() -> AgentSettings:
    return AgentSettings()
