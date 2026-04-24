from pydantic import BaseModel


class CreateLinkDTO(BaseModel):
    original_url: str
    # TODO: add alias field


class Link(BaseModel):
    slug: str
    original_url: str


class Pagination(BaseModel):
    limit: int = 100
    offset: int = 0


class RequestInfo(BaseModel):
    ip: str
    agent: str


class RedirectRequestInfo(RequestInfo):
    slug: str
