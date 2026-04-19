from fastapi import APIRouter, Depends

from .dependencies import get_service, get_request_info
from .service import ShortenerService
from .schemas import CreateLinkDTO, Pagination

from core.rabbit import get_publisher, RabbitPublisher

sh_router = APIRouter(prefix="/sh", tags=["shortener"])


@sh_router.get("/")
async def get_all(
    pagination=Depends(Pagination), service: ShortenerService = Depends(get_service)
):
    return await service.get_links(limit=pagination.limit, offset=pagination.offset)


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
    body: CreateLinkDTO, service: ShortenerService = Depends(get_service)
):
    return await service.create_link(body)


@sh_router.delete("/delete/{slug}")
async def delete_by_id(slug: str, service: ShortenerService = Depends(get_service)):
    return await service.delete_by_slug(slug)
