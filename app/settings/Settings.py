from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    ALGORITHM: str
    SECRET_KEY: str
    DATABASE_URL: str


def get_settings():
    return Settings()  # type: ignore
