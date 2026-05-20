from fastapi import Request, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from typing import Callable
from hashlib import sha256

from core.logger import get_logger

LIMITER_TTL = 30  # Timeout seconds
LIMITER_COUNT = 100  # Count of requests before blocking


def ratelimiter(ttl: int = LIMITER_TTL, limit: int = LIMITER_COUNT):
    async def limit_rate(req: Request, next: Callable):
        logger = get_logger(__name__)()

        ip = req.client.host
        redis: Redis = req.app.state.redis_pool
        hashed_ip = sha256(ip.encode("utf-8")).hexdigest()
        # TODO: move key to constants
        key = f"app:ratelimit:{hashed_ip}"
        calls_count = await redis.get(key)
        if calls_count is None:
            await redis.set(key, 0, ex=ttl)
        current_calls = await redis.incr(key, 1)
        if current_calls >= limit:
            logger.info(f"Blocked: {hashed_ip}. Reason: Too many requests")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests. Try again later."},
            )
        response = await next(req)
        return response

    return limit_rate
