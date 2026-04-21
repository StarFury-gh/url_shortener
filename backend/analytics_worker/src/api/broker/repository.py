from asyncpg import Connection

from .schemas import ClicksCount


class WorkerRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    async def get_stats(self, slug: str) -> ClicksCount | None:
        record = await self.db.fetchrow(
            "SELECT clicked_times FROM clicks WHERE slug=$1", slug
        )
        if record:
            return ClicksCount(**dict(record), slug=slug)
        return None

    async def update_agent_stats(
        self, slug: str, browser: str, os: str, device: str, raw_agent: str
    ):
        """Create or update clicks_count about redirect by slug agent"""
        await self.db.execute(
            """
            INSERT INTO users_agents (slug, browser, os, device_type, raw_str, clicks_count) 
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (raw_str) DO UPDATE SET
                clicks_count=users_agents.clicks_count+1
            """,
            slug,
            browser,
            os,
            device,
            raw_agent,
            0,
        )

    async def create_link_stats(self, slug: str) -> None:
        """Init slug counter"""
        await self.db.execute(
            "INSERT INTO clicks (slug, clicked_times) VALUES ($1, $2)", slug, 0
        )

    async def inc_clicks_count(self, slug: str) -> None:
        """Increment slug clicks counter"""
        await self.db.execute(
            "UPDATE clicks SET clicked_times=clicked_times+1 WHERE slug=$1", slug
        )

    async def delete_link_stats(self, slug: str):
        """Delete stats record about deleted slug"""
        await self.db.execute("DELETE FROM clicks WHERE slug=$1", slug)
        await self.db.execute("DELETE FROM users_agents WHERE slug=$1", slug)
