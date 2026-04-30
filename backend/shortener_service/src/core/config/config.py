from dotenv import load_dotenv
from os import getenv


class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.DB_HOST = getenv("DB_HOST")
        self.DB_PORT = getenv("DB_PORT")
        self.DB_USER = getenv("DB_USER")
        self.DB_PASSWORD = getenv("DB_PASSWORD")
        self.DB_NAME = getenv("DB_NAME")
        self.PG_DSN = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

        self.RMQ_HOST = getenv("RMQ_HOST")
        self.RMQ_PORT = getenv("RMQ_PORT")
        self.RMQ_USER = getenv("RMQ_USER")
        self.RMQ_PASSWORD = getenv("RMQ_PASSWORD")
        self.RMQ_DSN = f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}:{self.RMQ_PORT}"

        self.REDIS_HOST = getenv("REDIS_HOST")
        self.REDIS_PORT = getenv("REDIS_PORT")
        self.REDIS_PASSWORD = getenv("REDIS_PASSWORD")
        self.REDIS_USER = getenv("REDIS_USER")
        self.REDIS_DSN = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}@{self.REDIS_USER}:{self.REDIS_PASSWORD}"


cfg_obj = Config()
