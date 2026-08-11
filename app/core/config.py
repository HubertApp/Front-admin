from pydantic_settings import BaseSettings, SettingsConfigDict

class Secrets(BaseSettings):
    GATEWAY_KEY: str = "<TOKEN>"
    SECRET_KEY: str = "<SECRET>"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
secrets = Secrets()

class Properties(BaseSettings):
    APP_NAME: str = "HubberApp Admin Website"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    URL_GATEWAY: str = "http://localhost:8000"
    model_config = SettingsConfigDict(
        env_file="application.properties",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
properties = Properties()