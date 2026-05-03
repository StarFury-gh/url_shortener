from fastapi import Request


async def get_redis(r: Request):
    return r.app.state.redis_pool
