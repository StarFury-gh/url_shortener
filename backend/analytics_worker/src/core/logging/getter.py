from os import getenv
from dotenv import load_dotenv
from logging import Logger

from common.enums import EnvEnum

from .json_logger import get_json_logger
from .text_logger import get_text_logger

load_dotenv()


def get_logger(name: str = "analytics_worker") -> Logger:
    env_type = getenv("ENV_TYPE")
    if env_type is None:
        print("WARNING: ENV VARIABLE 'ENV_TYPE' is not provided, using: LOCAL")
        env_type = EnvEnum.LOCAL.value

    env_type = env_type.lower()
    if env_type == EnvEnum.DEV.value or env_type == EnvEnum.LOCAL.value:
        logger = get_text_logger(name)
        return logger
    elif env_type == EnvEnum.PROD:
        logger = get_json_logger(name)
        return logger

    else:
        return get_text_logger(name)
