from fastapi import HTTPException, status
from hashlib import sha256

from .repository import UsersRepository
from .schemas import UserLogin, RegisterUser


class UsersService:
    def __init__(self, repo: UsersRepository) -> None:
        self.repo = repo

    async def get_all(self) -> dict:
        users = await self.repo.get_all()
        return {"users": users}

    async def get_by_id(self, id: int) -> dict:
        user = await self.repo.get(id)
        return {"user": user}

    async def delete(self, id: int) -> dict:
        user = await self.repo.delete(id)
        return {"status": True, "deleted": user}

    async def login(self, body: UserLogin):
        pass

    async def register(self, body: RegisterUser) -> dict:
        hashed_password = sha256(body.password.encode("utf-8")).hexdigest()
        user = RegisterUser(email=body.email, password=hashed_password)
        try:
            result = await self.repo.create(user)
            return {"status": True, "user_id": result}
        except:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
