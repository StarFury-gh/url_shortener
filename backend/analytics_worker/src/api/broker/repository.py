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

    async def create_link_stats(self, slug: str) -> None:
        await self.db.execute(
            "INSERT INTO clicks (slug, clicked_times) VALUES ($1, $2)", slug, 0
        )

    async def get_by_slug(self, slug: str):
        pass

    async def get_all(self):
        pass

    async def delete_link_stats(self, slug: str):
        await self.db.execute("DELETE FROM clicks WHERE slug=$1", slug)
