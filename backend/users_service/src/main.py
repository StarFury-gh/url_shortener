from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager

from core.db.postgres import craete_pg_pool

from api.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_pool = await craete_pg_pool()
    app.state.pg_pool = pg_pool
    yield
    await app.state.pg_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
