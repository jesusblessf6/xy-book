from functools import lru_cache

from xybook_common.config import ServiceSettings


class ExperimentSettings(ServiceSettings):
    service_name: str = "experiments"
    service_port: int = 8005
    database_url: str = "postgresql+asyncpg://wing@localhost:5432/experiments"


@lru_cache
def get_settings() -> ExperimentSettings:
    return ExperimentSettings()
