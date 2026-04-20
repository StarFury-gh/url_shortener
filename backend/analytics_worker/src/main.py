from fastapi import FastAPI
from uvicorn import run

from asyncio import wait_for

from contextlib import asynccontextmanager

from core.db.postgres import create_pg_pool
from api.broker import msg_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_pool = await create_pg_pool()
    app.state.pg_pool = pg_pool
    yield
    await wait_for(app.state.pg_pool.close(), timeout=10)


app = FastAPI(lifespan=lifespan)
app.include_router(msg_router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
