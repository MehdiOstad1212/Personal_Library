from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLAlCHEMY_DATABASE_URL: str = "sqlite:///:memory:"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()