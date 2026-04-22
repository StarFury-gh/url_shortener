from fastapi import Request


async def get_pg(r: Request):
    async with r.app.state.pg_pool.acquire() as conn:
        yield conn
