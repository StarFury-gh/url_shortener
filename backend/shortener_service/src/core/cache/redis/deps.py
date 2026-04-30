from fastapi import Request
from redis.asyncio import Redis


async def get_redis(r: Request):
    return r.app.state.redis_pool
