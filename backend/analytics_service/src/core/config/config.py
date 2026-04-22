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


cfg_obj = Config()
