from asyncpg import create_pool

from core.config import cfg_obj


async def create_pg_pool():
    return await create_pool(cfg_obj.PG_DSN)
