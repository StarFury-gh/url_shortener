from fastapi import Request
from asyncpg import Connection


async def get_pg(r: Request) -> Connection:
    return await r.app.state.pg_pool.aquire()
