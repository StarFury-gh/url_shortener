from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0


class BrowserAgent(BaseModel):
    browser: str
    device_type: str
    os: str
    clicks_count: int


class FullSlugInfo(BaseModel):
    slug: str
    clicked_times: int | None
    agents: list[BrowserAgent]
