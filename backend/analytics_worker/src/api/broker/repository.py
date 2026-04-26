from asyncpg import Connection

from .schemas import ClicksCount


class WorkerRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    async def get_stats(self, slug: str) -> ClicksCount | None:
        record = await self.db.fetchrow(
            "SELECT clicks_count FROM clicks WHERE slug=$1", slug
        )
        if record:
            return ClicksCount(**dict(record), slug=slug)
        return None

    async def _update_browser_clicks(self, slug: str, browser: str) -> None:
        await self.db.execute(
            """
            INSERT INTO users_agents AS ua (slug, browser, clicks_count, raw_stat) 
            VALUES ($1, $2, $3, $4) 
            ON CONFLICT(raw_stat) 
            DO UPDATE SET clicks_count=ua.clicks_count+1
            """,
            slug,
            browser,
            1,
            slug + browser,
        )

    async def _update_os_clicks(self, slug: str, os: str) -> None:
        await self.db.execute(
            """
            INSERT INTO users_os AS uo (slug, os, clicks_count, raw_stat)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (raw_stat)
            DO UPDATE SET clicks_count=uo.clicks_count+1
            """,
            slug,
            os,
            1,
            slug + os,
        )

    async def _update_device_clicks(self, slug, device: str) -> None:
        await self.db.execute(
            """
            INSERT INTO users_devices AS ud (slug, device_type, clicks_count, raw_stat)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (raw_stat)
            DO UPDATE SET clicks_count=ud.clicks_count+1
            """,
            slug,
            device,
            1,
            slug + device,
        )

    async def update_agent_stats(
        self, slug: str, browser: str, os: str, device: str
    ) -> None:
        """Create or update clicks_count about redirect by slug agent"""
        await self._update_browser_clicks(slug, browser)
        await self._update_device_clicks(slug, device)
        await self._update_os_clicks(slug, os)

    async def create_link_stats(self, slug: str) -> None:
        """Init slug counter"""
        await self.db.execute(
            "INSERT INTO clicks (slug, clicks_count) VALUES ($1, $2)", slug, 0
        )

    async def inc_clicks_count(self, slug: str) -> None:
        """Increment slug clicks counter"""
        await self.db.execute(
            "UPDATE clicks SET clicks_count=clicks_count+1 WHERE slug=$1", slug
        )

    async def delete_link_stats(self, slug: str):
        """Delete stats record about deleted slug"""
        await self.db.execute("DELETE FROM clicks WHERE slug=$1", slug)
        await self.db.execute("DELETE FROM users_agents WHERE slug=$1", slug)
