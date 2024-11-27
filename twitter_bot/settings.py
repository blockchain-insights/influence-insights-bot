import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

load_dotenv()
class Settings(BaseSettings):
    FETCH_API_BASE_URL: str

    TWEET_GENERATION_INTERVAL_HOURS: int
    SUSPICIOUS_TWEET_INTERVAL_HOURS: int
    TWEET_POSTING_INTERVAL_HOURS: int
    TWEET_POSTING_DELAY_SECONDS: int
    TRIGGER_IMMEDIATE: bool

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_URL: str

    TWITTER_API_KEY: str
    TWITTER_API_SECRET_KEY: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN_SECRET: str
    TWITTER_BEARER_TOKEN: str
    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str

    DB_URL_OBJ: URL = URL.create(
        "postgresql+asyncpg",
        username=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DB")
    )

    DATABASE_URL: str = f"{DB_URL_OBJ.drivername}://{DB_URL_OBJ.username}:{DB_URL_OBJ.password}@{DB_URL_OBJ.host}:{DB_URL_OBJ.port}/{DB_URL_OBJ.database}"
    PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
    model_config = SettingsConfigDict(env_file=".env", extra='allow')


settings = Settings()
