from pydantic import BaseModel


class CreateLinkDTO(BaseModel):
    original_url: str
    # TODO: add alias field


class Link(BaseModel):
    slug: str
    original_url: str
