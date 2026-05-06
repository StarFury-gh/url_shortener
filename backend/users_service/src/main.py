from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "frontend:80",
        "frontend:8080",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
