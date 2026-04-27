from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0


class BrowserAgent(BaseModel):
    """Info about agent's browser"""

    browser: str
    clicks_count: int


class AgentOs(BaseModel):
    """Info about agent's os"""

    os: str
    clicks_count: int


class AgentDevice(BaseModel):
    """Info about agent's device type"""

    device_type: str
    clicks_count: int


class FullSlugInfo(BaseModel):
    """Full info about slug's redirects"""

    slug: str
    clicks_count: int | None
    agents: list[BrowserAgent]
    os: list[AgentOs]
    devices: list[AgentDevice]
