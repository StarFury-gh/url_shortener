from fastapi import HTTPException, status

from user_agents import parse

from .repository import WorkerRepository
from .schemas import LinkAction, ClickInfo


class WorkerService:
    def __init__(self, repo: WorkerRepository) -> None:
        self._repo = repo

    async def handle_link_operation(self, message: LinkAction) -> None:
        if message.operation == "created":
            await self._repo.create_link_stats(message.slug)
        elif message.operation == "deleted":
            await self._repo.delete_link_stats(message.slug)

    async def get_link_stats(self, slug: str) -> dict:
        stats = await self._repo.get_stats(slug)
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Link is not found"
            )
        return {"slug": slug, "clicked_times": stats.clicked_times}

    async def handle_link_redirect(self, msg: ClickInfo) -> None:
        agent_info = parse(msg.agent)

        browser_version = ".".join(list(map(str, agent_info.browser.version)))
        browser = " ".join([agent_info.browser.family, browser_version])

        os_version = ".".join(list(map(str, agent_info.os.version_string)))
        os = " ".join([agent_info.os.family, os_version])

        device = agent_info.device.family

        await self._repo.update_agent_stats(
            slug=msg.slug,
            browser=browser,
            os=os,
            device=device,
            raw_agent=str(agent_info),
        )
        await self._repo.inc_clicks_count(slug=msg.slug)
