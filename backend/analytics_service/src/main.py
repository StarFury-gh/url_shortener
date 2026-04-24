from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from contextlib import asynccontextmanager

from core.db.postgres import create_pg_pool
from api.analytics import an_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pg_pool = await create_pg_pool()
    yield
    await app.state.pg_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(an_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://frontend:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
