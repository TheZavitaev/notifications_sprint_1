from pydantic.env_settings import BaseSettings
from pydantic.networks import PostgresDsn


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/notifications'
    POSTGRES_BACKOFF_MAX_TIME: int = 50
    USER_SERVICE_URL: str = 'http://127.0.0.1:8002/api/v1/'
    USER_SERVICE_BACKOFF_MAX_TIME: int = 50
    WORKER_SLEEP_TIME: int = 1

    EMAIL_SENDER_TYPE: str = 'fake'
    DATA_SOURCE_TYPE: str = 'fake'

    SENDGRID_API_KEY: str = 'secret_key'
    SENDGRID_FROM_EMAIL: str = 'practix.notifications@gmail.com'

config = Config()
