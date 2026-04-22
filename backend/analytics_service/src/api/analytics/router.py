from fastapi import APIRouter, Depends

from .dependencies import get_service
from .service import AnalyticsService

an_router = APIRouter(prefix="/analytics", tags=["analytics"])


@an_router.get("/agents")
async def get_popular_agents(service: AnalyticsService = Depends(get_service)):
    return await service.get_popular_agents()


@an_router.get("/{slug}")
async def get_slug_stats(slug: str, service: AnalyticsService = Depends(get_service)):
    return await service.get_full_slug_info(slug)
