"""Typed application settings."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NEXUS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    service_name: str = "nexus-intelligence-cloud"
    log_level: str = "INFO"
    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    allowed_origins: str = "http://localhost:3000"

    # Model serving stays disabled until an operator configures the private backend and key.
    gateway_enabled: bool = False
    gateway_api_key: SecretStr = SecretStr("")
    vllm_base_url: str = "http://127.0.0.1:8001"
    model_id: str = "Qwen/Qwen2.5-7B-Instruct"
    model_request_timeout: float = Field(default=90.0, gt=0, le=600)
    max_concurrent_generations: int = Field(default=4, ge=1, le=128)
    gateway_queue_timeout: float = Field(default=5.0, gt=0, le=60)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
