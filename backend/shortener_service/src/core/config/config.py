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


cfg_obj = Config()
