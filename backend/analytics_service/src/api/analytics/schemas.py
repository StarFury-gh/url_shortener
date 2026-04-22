from pydantic import BaseModel
from typing import List


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0


class SlugAgent:
    browser: str
    device_type: str


class SlugInfo(BaseModel):
    slug: str
    clicked_times: int
    agents: List[SlugAgent]
