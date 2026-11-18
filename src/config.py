from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: SecretStr
    redis_url: SecretStr
    chroma_url: str
    ollama_url: str

    minio_endpoint: str
    minio_root_user: str
    minio_root_password: SecretStr
    minio_secure: bool
    minio_bucket: str

    ollama_chat_model: str
    ollama_embedding_model: str
    jwt_secret: SecretStr = Field(min_length=32, max_length=64)
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_minutes: int = Field(gt=0, default=30)


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
