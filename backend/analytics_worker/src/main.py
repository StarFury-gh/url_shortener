from fastapi import FastAPI
from uvicorn import run

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_pool = 
    yield


app = FastAPI()

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)
