from fastapi import Depends

from core.db.postgres import get_pg
from .repository import AnalyticsRepository
from .service import AnalyticsService


def get_analytics_repo(pg=Depends(get_pg)):
    return AnalyticsRepository(pg)


def get_service(repo: AnalyticsRepository = Depends(get_analytics_repo)):
    return AnalyticsService(repo)
