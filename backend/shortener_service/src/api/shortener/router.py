from fastapi import APIRouter, Depends

from .dependencies import get_service
from .service import ShortenerService
from .schemas import CreateLinkDTO

sh_router = APIRouter(prefix="/sh", tags=["shortener"])


@sh_router.get("/{slug}")
async def get_and_redirect(slug: str, service: ShortenerService = Depends(get_service)):
    return await service.get_and_redirect(slug)


@sh_router.post("/create")
async def create_short_link(
    body: CreateLinkDTO, service: ShortenerService = Depends(get_service)
):
    return await service.create_link(body)


@sh_router.delete("/delete/{id}")
async def delete_by_id(id: int):
    pass
