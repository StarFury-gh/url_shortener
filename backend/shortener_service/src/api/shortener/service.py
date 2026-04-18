from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from asyncpg.exceptions import UniqueViolationError

from hashlib import sha256

from core.utils import is_valid_url

from .repository import ShortenerRepository
from .schemas import CreateLinkDTO


class ShortenerService:
    def __init__(self, repo: ShortenerRepository) -> None:
        self.repo = repo

    async def get_and_redirect(self, slug: str):
        link = await self.repo.get(slug)
        if link:
            return RedirectResponse(link.original_url)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    async def create_link(self, body: CreateLinkDTO):
        try:
            if not is_valid_url(body.original_url):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url"
                )
            slug = sha256(body.original_url.encode("utf-8")).hexdigest()[:12]
            link = await self.repo.get(slug)
            if not link:
                await self.repo.create(original_url=body.original_url, slug=slug)
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
