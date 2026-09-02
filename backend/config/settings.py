from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ALICE AI"
    environment: str = "development"
    debug: bool = True
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-luna"
    llm_timeout_seconds: float = 30.0
    database_path: str = "data/database/alice.db"
    max_conversation_messages: int = 20
    cors_origins: str = "*"

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
