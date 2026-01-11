from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "HOTFIX INCIDENT COPILOT"
    VERSION: str = "0.1.0"
    API_VERSION: str = "/api/v1"

    AI_API_KEY: str = "mock-key"
    AI_MODEL: str = "gpt-5-mini"
    AI_TEMPERATURE: float = 1.0

    LOG_LEVEL: str = "INFO"

    ALLOWED_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
