from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ALICE AI"
    environment: str = "development"
    debug: bool = False
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-luna"
    llm_timeout_seconds: float = Field(default=30.0, gt=0, le=120)
    database_path: str = "data/database/alice.db"
    rag_database_path: str = "data/database/alice_rag.db"
    max_conversation_messages: int = Field(default=20, ge=1, le=100)
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    api_key: str | None = None
    rate_limit_per_minute: int = Field(default=60, ge=1, le=10000)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
