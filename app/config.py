from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App config loaded from environment / .env file.

    pydantic-settings validates types at startup, so a missing or malformed
    DATABASE_URL fails loudly here instead of mysteriously deep in the app.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    arxiv_category: str = "cs.AI"
    ingest_pages: int = 3


settings = Settings()
