from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HRM-BE"
    secret_key: str = "supersecretkey-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./hrms.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


