from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    service_name: str = "xybook"
    service_port: int = 8000
    database_url: str = "postgresql+asyncpg://xybook:xybook_dev@localhost:5432/xybook"
    redis_url: str = "redis://localhost:6379/0"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False

    model_config = {"env_prefix": "XYBOOK_", "env_file": ".env"}
