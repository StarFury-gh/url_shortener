from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class BaseUser(BaseModel):
    email: str


class UserLogin(BaseUser):
    password: str


class RegisterUser(BaseUser):
    password: str


class User(BaseUser):
    id: int
    created_at: datetime
    password: Optional[str | None] = None


class GetUsersResponse(BaseModel):
    users: List[User]


class GetUserByIdResponse(BaseModel):
    user: User
