from fastapi import Depends

from core.db.postgres import get_pg

from .repository import WorkerRepository
from .service import WorkerService


async def get_repo(pg=Depends(get_pg)):
    return WorkerRepository(pg)


async def get_service(repo=Depends(get_repo)):
    return WorkerService(repo)
