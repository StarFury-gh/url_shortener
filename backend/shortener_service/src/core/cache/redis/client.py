"""
Application-level Redis client — initialized once at startup.
"""

from __future__ import annotations

from core.config import cfg_obj

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

_redis_client: Redis | None = None


def create_redis_pool(
    url: str | None = None,
    max_connections: int = 20,
    decode_responses: bool = True,
) -> Redis:
    resolved_url = url or cfg_obj.REDIS_DSN
    pool = ConnectionPool.from_url(
        resolved_url,
        max_connections=max_connections,
        decode_responses=decode_responses,
    )
    return Redis(connection_pool=pool)


def get_redis() -> Redis:
    if _redis_client is None:
        raise RuntimeError(
            "Redis client is not initialised. "
            "Call `init_redis()` during application startup."
        )
    return _redis_client


async def init_redis(url: str | None = None) -> Redis:
    global _redis_client  # noqa: PLW0603
    _redis_client = create_redis_pool(url=url)
    await _redis_client.ping()
    return _redis_client


async def close_redis() -> None:
    global _redis_client  # noqa: PLW0603
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
