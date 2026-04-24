from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from contextlib import asynccontextmanager

from core.db.postgres import create_pg_pool
from core.rabbit import create_rmq_connection
from api.shortener import sh_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_pool = await create_pg_pool()
    rabbit = await create_rmq_connection()
    app.state.pg_pool = pg_pool
    app.state.rabbit = rabbit
    yield
    await app.state.rabbit.stop()
    await app.state.pg_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(sh_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "frontend:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
