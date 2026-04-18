from fastapi import Depends
from core.db.postgres import get_pg

from .repository import ShortenerRepository
from .service import ShortenerService


async def get_repo(pg_conn=Depends(get_pg)):
    return ShortenerRepository(pg_conn)


async def get_service(repo=Depends(get_repo)):
    return ShortenerService(repo)
