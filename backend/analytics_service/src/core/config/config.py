from dotenv import load_dotenv
from os import getenv


class Config:
    def __init__(self):
        load_dotenv()
        self.PG_HOST = getenv("PG_HOST")
        self.PG_PORT = getenv("PG_PORT")
        self.PG_USER = getenv("PG_USER")
        self.PG_PASSWORD = getenv("PG_PASSWORD")
        self.PG_NAME = getenv("PG_NAME")
        self.PG_DSN = f"postgres://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"

        self.USERS_SERVICE = getenv("USERS_SERVICE")

        self.REDIS_HOST = getenv("REDIS_HOST")
        self.REDIS_PORT = getenv("REDIS_PORT")
        self.REDIS_PASSWORD = getenv("REDIS_PASSWORD")
        self.REDIS_USER = getenv("REDIS_USER")
        self.REDIS_DSN = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"


cfg_obj = Config()
