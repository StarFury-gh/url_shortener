from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0


class BrowserAgent(BaseModel):
    browser: str
    clicks_count: int


class AgentOs(BaseModel):
    os: str
    clicks_count: int


class AgentDevice(BaseModel):
    device_type: str
    clicks_count: int


class FullSlugInfo(BaseModel):
    slug: str
    clicks_count: int | None
    agents: list[BrowserAgent]
    os: list[AgentOs]
    devices: list[AgentDevice]
