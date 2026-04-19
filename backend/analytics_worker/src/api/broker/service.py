from fastapi import HTTPException, status

from .repository import WorkerRepository
from .schemas import LinkAction


class WorkerService:
    def __init__(self, repo: WorkerRepository) -> None:
        self._repo = repo

    async def handle_link_action(self, message: LinkAction) -> None:
        if message.operation == "created":
            await self._repo.create_link_stats(message.slug)
        elif message.operation == "deleted":
            await self._repo.delete_link_stats(message.slug)

    async def get_link_stats(self, slug: str):
        stats = await self._repo.get_stats(slug)
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link is not found"
            )
        return {"slug": slug, "clicked_times": stats.clicked_times}
