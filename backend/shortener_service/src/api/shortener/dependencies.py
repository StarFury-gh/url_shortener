from fastapi import Depends, Request, Header
from core.db.postgres import get_pg

from .repository import ShortenerRepository
from .service import ShortenerService
from .schemas import RequestInfo, AuthUserResponse


async def get_repo(pg_conn=Depends(get_pg)):
    return ShortenerRepository(pg_conn)


async def get_service(repo=Depends(get_repo)):
    return ShortenerService(repo)


async def get_request_info(r: Request) -> RequestInfo:
    result = RequestInfo(ip=r.client.host, agent=r.headers.get("user-agent", "Unknown"))
    return result


async def get_auth(authorization: str = Header(None)) -> AuthUserResponse | None:
    """Check user's authorization.

    Args:
        authorization (str): 'Authorization' header with jwt

    Returns:
        AuthUserResponse | None: AuthUserResponse contains info about user (got from users_service)
        None - if user didn't provide header
    """
    if authorization is None:
        return None

    authorization = authorization.strip()

    if not authorization:
        return None

    # TODO: change placeholder to real request

    # aiohttp.request to users_service/users/auth

    data = {"id": 1, "email": "testemail@mail.ru"}

    return AuthUserResponse(**data)
