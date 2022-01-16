from pydantic.env_settings import BaseSettings


class Config(BaseSettings):
    PUBLISHER_CHUNK_SIZE: int = 5


config = Config()
