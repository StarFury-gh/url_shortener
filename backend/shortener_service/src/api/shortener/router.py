from fastapi import APIRouter, Depends

from .dependencies import get_service, get_request_info, get_auth
from .service import ShortenerService
from .schemas import CreateLinkDTO, Pagination, AuthUserResponse

from core.rabbit import get_publisher, RabbitPublisher
from core.cache.redis import get_redis
from core.logger import get_logger

sh_router = APIRouter(prefix="/sh", tags=["shortener"])


@sh_router.get("/")
async def get_all(
    pagination=Depends(Pagination),
    service: ShortenerService = Depends(get_service),
    auth=Depends(get_auth),
):
    return await service.get_links(
        limit=pagination.limit, offset=pagination.offset, auth=auth
    )


@sh_router.get("/{slug}")
async def get_and_redirect(
    slug: str,
    service: ShortenerService = Depends(get_service),
    req_info=Depends(get_request_info),
    broker: RabbitPublisher = Depends(get_publisher),
):
    return await service.get_and_redirect(slug, broker=broker, info=req_info)


@sh_router.post("/create")
async def create_short_link(
    body: CreateLinkDTO,
    service: ShortenerService = Depends(get_service),
    auth: AuthUserResponse = Depends(get_auth),
    broker=Depends(get_publisher),
    redis=Depends(get_redis),
    app_logger=Depends(get_logger),
):
    return await service.create_link(
        body, broker=broker, redis=redis, app_logger=app_logger, auth=auth
    )


@sh_router.delete("/delete/{slug}")
async def delete_by_id(
    slug: str,
    service: ShortenerService = Depends(get_service),
    broker=Depends(get_publisher),
):
    return await service.delete_by_slug(slug, broker=broker)
