from pydantic.env_settings import BaseSettings
from pydantic.networks import PostgresDsn


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/notifications'
    PUBLISHER_CHUNK_SIZE: int = 5
    SELECT_BATCH_SIZE: int = 10
    SCHEDULER_SLEEP_TIME: int = 5
    POSTGRES_BACKOFF_MAX_TIME: int = 50


config = Config()
