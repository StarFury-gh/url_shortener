from pydantic import BaseModel


class ClickInfo(BaseModel):
    ip: str
    agent: str
    slug: str


class LinkAction(BaseModel):
    operation: str
    slug: str


class ClicksCount(BaseModel):
    slug: str
    clicked_times: int
