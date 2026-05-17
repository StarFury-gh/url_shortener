from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from asyncpg.exceptions import UniqueViolationError
from redis.asyncio import Redis

from logging import Logger

from core.utils import is_valid_url, generate_new_slug
from core.utils import constants
from core.rabbit import RabbitPublisher
from core.rabbit.schemas import RedirectRequestInfo

from .repository import ShortenerRepository
from .schemas import CreateLinkDTO, AuthUserResponse


class ShortenerService:
    def __init__(self, repo: ShortenerRepository) -> None:
        self.repo = repo

    async def get_links(
        self,
        auth: AuthUserResponse | None,
        limit: int = 10,
        offset: int = 0,
    ):
        if auth is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden for you"
            )
        links = await self.repo.get_all(limit=limit, offset=offset, author_id=auth.id)
        return {"links": links, "total": len(links)}

    async def get_and_redirect(
        self, slug: str, broker: RabbitPublisher, info: RedirectRequestInfo
    ):
        link = await self.repo.get(slug)

        if link:
            # Message about redirect
            message = RedirectRequestInfo(slug=slug, ip=info.ip, agent=info.agent)
            # Send this message to another microservice: "Look, somebody was redirected by short link
            # redirect info is: ..."
            await broker.handle_redirect(message)
            return RedirectResponse(link.original_url)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    async def create_link(
        self,
        body: CreateLinkDTO,
        broker: RabbitPublisher,
        redis: Redis,
        app_logger: Logger,
        auth: AuthUserResponse,
    ):
        try:
            if not is_valid_url(body.original_url):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url"
                )

            original_url = body.original_url.strip("/")
            # Get previous generated slug from Redis
            prev_slug_bytes = await redis.get(constants.REDIS_SLUG_KEY)
            # If it is the first request, we will get None
            if prev_slug_bytes is None:
                prev_slug = prev_slug_bytes
            # Else, we get raw str, encode it to utf-8
            else:
                prev_slug = prev_slug_bytes.decode("utf-8")

            # Generate new slug using previous
            slug = await generate_new_slug(prev_slug=prev_slug)
            app_logger.info(f"Generated new slug: {slug}; prev_slug is: {prev_slug}")
            # Check if slug already exists
            # TODO: use this only for auth users
            link = await self.repo.get(slug)

            app_logger.info(
                f"Created new link with slug: {slug}, original_url: {body.original_url}"
            )

            if not link:

                if auth is None:
                    auth_id = None
                else:
                    auth_id = auth.id

                await self.repo.create(
                    original_url=original_url, slug=slug, author_id=auth_id
                )
                # Send message to another microservice: "User created new short link,
                # please, create record about this in analytics db"
                await broker.publish(
                    {"operation": "created", "slug": slug, "author": auth_id},
                    queue="links_actions",
                )

            # Save new slug to the Redis
            await redis.set(constants.REDIS_SLUG_KEY, slug)
            return {"slug": slug}

        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Slug already exists"
            )

        except HTTPException as e:
            raise e

        except Exception as e:
            app_logger.error(e)
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

        # Send message about deleting to another microservice
        await broker.publish(
            {"operation": "deleted", "slug": slug}, queue="links_actions"
        )

        return {"deleted": slug, "origin": result}
