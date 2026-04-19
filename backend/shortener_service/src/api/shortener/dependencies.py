from fastapi import Depends, Request
from core.db.postgres import get_pg

from .repository import ShortenerRepository
from .service import ShortenerService
from .schemas import RequestInfo


async def get_repo(pg_conn=Depends(get_pg)):
    return ShortenerRepository(pg_conn)


async def get_service(repo=Depends(get_repo)):
    return ShortenerService(repo)


async def get_request_info(r: Request) -> RequestInfo:
    result = RequestInfo(ip=r.client.host, agent=r.headers.get("user-agent", "Unknown"))
    return result
