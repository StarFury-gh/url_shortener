from redis.asyncio import Redis
from asyncpg import Pool
from api.shortener.repository import ShortenerRepository
from core.utils import constants
from core.logger import get_logger


async def sync_slugs(redis: Redis, db_pool: Pool) -> None:
    logger = get_logger(__name__)
    db_conn = await db_pool.acquire()
    repo = ShortenerRepository(db_conn)
    last_slug = await repo.get_last_slug()
    if last_slug is not None:
        logger.info(f"Last slug was synchronized. Current slug is: {last_slug}")
        await redis.set(constants.REDIS_SLUG_KEY, last_slug)

    else:
        logger.info("Last slug is None. No one short link detected.")
