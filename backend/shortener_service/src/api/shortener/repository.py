from asyncpg import Connection
from typing import List
from .schemas import Link


class ShortenerRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    async def get(self, slug: str) -> Link | None:
        """Return shortified link"""
        record = await self.db.fetchrow(
            "SELECT origin FROM short_urls WHERE slug=$1", slug
        )
        if record is not None:
            info = dict(record)
            result = Link(slug=slug, original_url=info.get("origin"))  # type: ignore
            return result
        return None

    async def get_all(self, limit: int, offset: int, author_id: int) -> List[Link]:
        """Return all shortified urls"""
        records = await self.db.fetch(
            "SELECT slug, origin FROM short_urls WHERE author_id=$1 LIMIT $2 OFFSET $3",
            author_id,
            limit,
            offset,
        )
        result = [dict(record) for record in records]
        result = [
            Link(slug=link.get("slug"), original_url=link.get("origin"))  # type: ignore
            for link in result
        ]
        return result

    async def create(self, slug: str, original_url: str, author_id: int | None) -> None:
        """Insert new short url to db"""
        await self.db.execute(
            "INSERT INTO short_urls (slug, origin, author_id) VALUES ($1, $2, $3)",
            slug,
            original_url,
            author_id,
        )

    async def delete(self, slug: str) -> str | None:
        """Delete an url by slug, returns original url of shortified version."""
        origin = await self.db.fetchval(
            "DELETE FROM short_urls WHERE slug=$1 RETURNING origin", slug
        )
        return origin

    async def get_last_slug(self) -> str | None:
        """Return last created slug"""
        slug = await self.db.fetchval(
            "SELECT * FROM short_urls ORDER BY created_at DESC LIMIT 1"
        )
        return slug
