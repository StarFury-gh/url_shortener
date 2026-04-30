import logging
import json
from pathlib import Path


def _get_settings(config_path: str = "./logger_config.json") -> dict:
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / config_path
    with open(config_path, "r") as file:
        config = json.load(file)

    return config


def get_logger(name: str = __name__) -> logging.Logger:
    logger_config = _get_settings()
    logging.config.dictConfig(logger_config)

    logger = logging.getLogger(name)

    return logger
