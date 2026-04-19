from pydantic import BaseModel


class ClickInfo(BaseModel):
    ip: str
    agent: str
    slug: str
