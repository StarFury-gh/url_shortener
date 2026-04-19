from pydantic import BaseModel


class RedirectRequestInfo(BaseModel):
    slug: str
    ip: str
    agent: str
