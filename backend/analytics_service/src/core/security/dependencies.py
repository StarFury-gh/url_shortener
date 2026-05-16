from fastapi import Header, Depends, HTTPException, status
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorDNSError

from core.logger import get_logger

from core.config import cfg_obj


async def require_auth(
    authorization=Header(None, alias="Authorization"), logger=Depends(get_logger)
) -> dict | None:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization required.",
        )

    async with ClientSession() as session:
        try:
            url = f"{cfg_obj.USERS_SERVICE}/users/auth"
            headers = {
                "Authorization": authorization,
                "Content-type": "application/json",
            }
            async with session.get(url, headers=headers) as response:
                if response.status:
                    result = await response.json()
                    return result
                text = await response.text()
                logger.error("Users service error:", text)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization required.",
                )
        except ClientConnectorDNSError as e:
            logger.error(e)
            return None
