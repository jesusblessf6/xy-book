from functools import lru_cache

from pydantic_settings import BaseSettings


class GatewaySettings(BaseSettings):
    service_port: int = 8000
    community_url: str = "http://localhost:8001"
    agents_url: str = "http://localhost:8002"
    pipeline_url: str = "http://localhost:8004"
    experiments_url: str = "http://localhost:8005"
    admin_api_key: str = "xybook-dev-key"

    model_config = {"env_prefix": "XYBOOK_GATEWAY_", "env_file": ".env"}


@lru_cache
def get_settings() -> GatewaySettings:
    return GatewaySettings()
