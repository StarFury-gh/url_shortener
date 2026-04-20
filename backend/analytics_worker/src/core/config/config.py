from dotenv import load_dotenv
from os import getenv


class Config:
    def __init__(self):
        load_dotenv()
        self.RMQ_USER = getenv("RMQ_USER")
        self.RMQ_PASSWORD = getenv("RMQ_PASSWORD")
        self.RMQ_HOST = getenv("RMQ_HOST")
        self.RMQ_PORT = getenv("RMQ_PORT")
        self.RMQ_DSN = f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}:{self.RMQ_PORT}"

        self.PG_USER = getenv("PG_USER")
        self.PG_PASSWORD = getenv("PG_PASSWORD")
        self.PG_HOST = getenv("PG_HOST")
        self.PG_PORT = getenv("PG_PORT")
        self.PG_NAME = getenv("PG_NAME")

        self.PG_DSN = f"postgres://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"


cfg_obj = Config()
