from fastapi import APIRouter, Depends

from .schemas import Pagination
from .dependencies import get_service
from .service import AnalyticsService

an_router = APIRouter(prefix="/analytics", tags=["analytics"])


@an_router.get("/{slug}")
async def get_slug_stats(slug: str, service: AnalyticsService = Depends(get_service)):
    pass


# TODO: add paginations
@an_router.get("/")
async def get_all_stats(
    pagination: Pagination = Depends(Pagination),
    service: AnalyticsService = Depends(get_service),
):
    return "Must return list of stats"


@an_router.get("/agents")
async def get_popular_agents(service: AnalyticsService = Depends(get_service)):
    return "Must return list of the most popular agents"
