from asyncpg import Connection

from .schemas import SlugInfo


class AnalyticsRepository:
    def __init__(self, db: Connection):
        self.db: Connection = db

    async def get_slug_info(self, slug: str) -> SlugInfo:
        record = await self.db.fetchrow("SELECT * FROM clicks")
