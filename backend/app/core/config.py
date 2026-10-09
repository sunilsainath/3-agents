"""Application configuration. Secrets come from env/secret manager only."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "MyTrakin API"
    app_version: str = "0.1.0"
    supabase_url: str = ""
    supabase_jwt_secret: str = ""
    supabase_jwt_audience: str = "authenticated"
    api_cors_origins: str = "http://localhost:3000"
    max_page_size: int = 100


settings = Settings()
