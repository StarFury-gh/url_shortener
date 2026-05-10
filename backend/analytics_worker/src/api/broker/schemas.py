from pydantic import BaseModel
from typing import Optional


class BrowserAgent(BaseModel):
    browser: str
    os: str
    device_type: str


class ClickInfo(BaseModel):
    ip: str
    agent: str
    slug: str


class LinkAction(BaseModel):
    operation: str
    slug: str
    author: Optional[int]


class ClicksCount(BaseModel):
    slug: str
    clicked_times: int
