from fastapi import Depends, Request, Header
from core.db.postgres import get_pg

from aiohttp import ClientSession

from logging import Logger

from core.config import cfg_obj
from core.logger import get_logger

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


async def get_auth(
    authorization: str = Header(None, alias="Authorization"),
    logger: Logger = Depends(get_logger),
) -> AuthUserResponse | None:
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

    async with ClientSession() as session:
        url = f"{cfg_obj.USERS_SERVICE}/users/auth"
        headers = {"Authorization": authorization}
        async with session.get(url, headers=headers) as response:
            if response.status:
                result = await response.json()
                return AuthUserResponse(**result)
            else:
                text = await response.text()
                logger.error(f"Error from USERS_SERVICE: {text}")
                return None
