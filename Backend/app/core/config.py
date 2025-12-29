# backend/app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str

    # OpenRouter / Embeddings
    openrouter_api_key: str
    openai_embed_model: str = "text-embedding-3-small"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"   # <--- IMPORTANT (default strict behavior)


settings = Settings()

