from asyncpg import Connection
from typing import List

from .schemas import FullSlugInfo, BrowserAgent


class AnalyticsRepository:
    def __init__(self, db: Connection):
        self.db: Connection = db

    async def get_slug_agents(self, slug: str) -> List[BrowserAgent]:
        records = await self.db.fetch(
            "SELECT browser, device_type, os, clicks_count FROM users_agents WHERE slug=$1",
            slug,
        )
        if records is None:
            return []
        records = [dict(record) for record in records]
        result = [BrowserAgent(**record) for record in records]
        return result

    async def get_slug_clicks_count(self, slug: str) -> int | None:
        record = await self.db.fetchval(
            "SELECT clicked_times FROM clicks WHERE slug=$1", slug
        )
        if record is None:
            return None
        return record

    async def get_full_slug_info(self, slug: str) -> FullSlugInfo:
        agents = await self.get_slug_agents(slug)
        clicks = await self.get_slug_clicks_count(slug)
        result = FullSlugInfo(slug=slug, agents=agents, clicked_times=clicks)
        return result

    async def get_popular_agents(self):
        records = await self.db.fetch(
            """
            SELECT 
            browser,
            SUM(clicks_count) AS total_clicks
            FROM users_agents
            GROUP BY browser
            ORDER BY total_clicks DESC;
            """
        )
        if records is None:
            return []

        result = [dict(record) for record in records]
        return result
