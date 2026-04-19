import logging
import logging.config
from pythonjsonlogger import jsonlogger

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


def get_json_logger(name: str) -> logging.Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)
    return logger
