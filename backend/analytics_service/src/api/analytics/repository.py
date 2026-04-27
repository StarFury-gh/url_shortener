from asyncpg import Connection
from typing import List

from .schemas import FullSlugInfo, BrowserAgent, AgentDevice, AgentOs


class AnalyticsRepository:
    def __init__(self, db: Connection):
        self.db: Connection = db

    async def get_slug_agents(self, slug: str) -> List[BrowserAgent]:
        """Return list of redirect agents

        Args:
            slug (str): short link's slug

        Returns:
            List[BrowserAgent]: all agents related with slug
        """
        records = await self.db.fetch(
            "SELECT browser, clicks_count FROM users_agents WHERE slug=$1",
            slug,
        )
        if records is None:
            return []
        records = [dict(record) for record in records]
        result = [BrowserAgent(**record) for record in records]
        return result

    async def get_slug_clicks_count(self, slug: str) -> int | None:
        """Return clicks by short link counter

        Args:
            slug (str): short link's slug

        Returns:
            int | None: clicks counter
        """
        record = await self.db.fetchval(
            "SELECT clicks_count FROM clicks WHERE slug=$1", slug
        )
        if record is None:
            return None
        return record

    async def get_slug_os(self, slug: str) -> List[AgentOs]:
        """Return list of redirect os

        Args:
            slug (str): short link's slug

        Returns:
            List[AgentOs]: all os related with slug
        """
        records = await self.db.fetch(
            "SELECT os, clicks_count FROM users_os WHERE slug=$1", slug
        )

        if records is None:
            return []

        records = [dict(record) for record in records]
        result = [AgentOs(**record) for record in records]
        return result

    async def get_slug_devices(self, slug: str) -> List[AgentDevice]:
        """_summary_

        Args:
            slug (str): short link's slug

        Returns:
            List[AgentDevice]: all devices types related with slug
        """
        records = await self.db.fetch(
            "SELECT device_type, clicks_count FROM users_devices WHERE slug=$1", slug
        )

        if records is None:
            return []

        records = [dict(record) for record in records]
        result = [AgentDevice(**record) for record in records]
        return result

    async def get_full_slug_info(self, slug: str) -> FullSlugInfo:
        """Return all analytics records related to slug

        Args:
            slug (str): short link's slug

        Returns:
            FullSlugInfo: analytics info about link
        """
        agents = await self.get_slug_agents(slug)
        os = await self.get_slug_os(slug)
        devices = await self.get_slug_devices(slug)
        clicks = await self.get_slug_clicks_count(slug)

        result = FullSlugInfo(
            slug=slug, agents=agents, clicks_count=clicks, os=os, devices=devices
        )
        return result

    async def get_popular_agents(self) -> List[BrowserAgent]:
        """Return the most popular agents
        Returns:
            List[BrowserAgent]: list of popular agents
        """
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
