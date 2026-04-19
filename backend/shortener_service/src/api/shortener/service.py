from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from asyncpg.exceptions import UniqueViolationError

from hashlib import sha256

from core.utils import is_valid_url
from core.rabbit import RabbitPublisher
from core.rabbit.schemas import RedirectRequestInfo

from .repository import ShortenerRepository
from .schemas import CreateLinkDTO


class ShortenerService:
    def __init__(self, repo: ShortenerRepository) -> None:
        self.repo = repo

    async def get_links(self, limit: int = 10, offset: int = 0):
        links = await self.repo.get_all()
        return {"links": links, "total": len(links)}

    async def get_and_redirect(
        self, slug: str, broker: RabbitPublisher, info: RedirectRequestInfo
    ):
        link = await self.repo.get(slug)
        if link:
            message = RedirectRequestInfo(slug=slug, ip=info.ip, agent=info.agent)
            await broker.handle_redirect(message)
            return RedirectResponse(link.original_url)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    async def create_link(self, body: CreateLinkDTO, broker: RabbitPublisher):
        try:
            if not is_valid_url(body.original_url):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url"
                )
            slug = sha256(body.original_url.encode("utf-8")).hexdigest()[:12]
            link = await self.repo.get(slug)
            if not link:
                await self.repo.create(original_url=body.original_url, slug=slug)
                await broker.publish(
                    {"operation": "created", "slug": slug}, queue="links_actions"
                )
            return {"slug": slug}
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Slug already exists"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    async def delete_by_slug(self, slug: str, broker: RabbitPublisher):
        result = await self.repo.delete(slug)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Url with slug is not found",
            )
        await broker.publish(
            {"operation": "deleted", "slug": slug}, queue="links_actions"
        )
        return {"deleted": slug, "origin": result}
