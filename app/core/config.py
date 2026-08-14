from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SentinelBank AI"
    app_env: str = "dev"
    database_url: str = "sqlite:///./sentinelbank.db"
    model_provider: str = "local"
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "amazon.nova-lite-v1:0"
    log_level: str = "INFO"
    api_key: str = "dev-analyst-key"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
