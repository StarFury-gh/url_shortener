from fastapi import HTTPException, status

from .repository import AnalyticsRepository
from .schemas import FullSlugInfo


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository):
        self._repo = repo

    async def get_full_slug_info(self, slug: str, auth: dict) -> FullSlugInfo:
        is_owner = await self._repo.check_ownership(slug, auth.get("id"))
        if is_owner:
            info = await self._repo.get_full_slug_info(slug)
            if info.clicks_count is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Link with this slug not found",
                )

            return info

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden for you"
        )

    async def get_popular_agents(self):
        info = await self._repo.get_popular_agents()

        return info
