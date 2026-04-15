from fastapi import Depends
from core.db.postgres import get_pg

from .repository import UsersRepository
from .service import UsersService


async def get_repo(pg_conn=Depends(get_pg)) -> UsersRepository:
    repo = UsersRepository(pg_conn)
    return repo


async def get_service(repo=Depends(get_repo)) -> UsersService:
    service = UsersService(repo)
    return service
