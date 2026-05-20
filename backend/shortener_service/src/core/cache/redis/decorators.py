from fastapi import Depends
from redis.asyncio import Redis

from functools import wraps
from typing import Callable
from hashlib import sha256
from json import dumps, loads
from logging import Logger

from core.logger import get_logger


from .client import get_redis


async def _stable_hash(value) -> str:
    raw = dumps(value, sort_keys=True, default=str)
    raw = raw.encode("utf-8")
    hashed_value = sha256(raw).hexdigest()[:16]
    return hashed_value


def _prepare_for_cache(obj):
    """Преобразует Pydantic модели в словари"""
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump()
    elif hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()
    elif isinstance(obj, list):
        return [_prepare_for_cache(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _prepare_for_cache(value) for key, value in obj.items()}
    return obj


async def _serialize(value) -> str:
    logger = get_logger(f"{__name__}:serializer")()
    result = dumps(value, default=str)
    logger.info(f"serializer: {value=} to {result=}; {type(result)=}")
    return result


async def _deserialize(value: str | bytes) -> dict:
    logger = get_logger(f"{__name__}:deserializer")()
    result = loads(value)
    logger.info(f"deserialized: {value=} to {result=}; {type(result)=}")
    return result


# app:shortener:module:name:args_hash:version
async def _create_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
    version: int = 1,
    skip_first_arg: bool = True,
) -> str:
    hashable_args = args[1:] if skip_first_arg and args else args
    payload = {"a": hashable_args, "b": kwargs}
    args_hash = await _stable_hash(payload)

    name = func.__name__
    module = func.__qualname__.split(".")[0]

    return f"app:shortener:{module}:{name}:{args_hash}:{version}"


def use_cache(ttl: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            logger: Logger = get_logger(__name__)(),
            **kwargs,
        ):
            redis: Redis = get_redis()

            key = await _create_key(func, args, kwargs)
            try:
                cached = await redis.get(key)

                if cached is not None:
                    result = await _deserialize(cached)
                    logger.info(f"Redis GET key: {key}. {result=}")
                    return result

                else:
                    result = await func(*args, **kwargs)

                    prepared_data = _prepare_for_cache(result)
                    json = await _serialize(prepared_data)
                    await redis.set(key, json, ex=ttl)
                    logger.info(f"Redis SET new key: {key}")

                    return result

            except Exception as e:
                logger.error(f"CACHE ERROR: {e}. KEY: {key}")
                result = await func(*args, **kwargs)
                return result

        return wrapper

    return decorator
