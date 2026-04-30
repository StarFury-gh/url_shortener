from redis.asyncio import Redis

from core.config import cfg_obj


async def create_redis_pool():
    pool = Redis(host=cfg_obj.REDIS_HOST, port=6379, password=cfg_obj.REDIS_PASSWORD)
    return pool
