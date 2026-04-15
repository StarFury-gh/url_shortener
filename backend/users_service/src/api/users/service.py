from fastapi import HTTPException, status
from hashlib import sha256
from hmac import compare_digest

from asyncpg.exceptions import UniqueViolationError

from core.tokens import encode_token

from .repository import UsersRepository
from .schemas import UserLogin, RegisterUser


class UsersService:
    def __init__(self, repo: UsersRepository) -> None:
        self.repo = repo

    def _create_hash(self, val: str) -> str:
        return sha256(val.encode("utf-8")).hexdigest()

    async def get_all(self) -> dict:
        users = await self.repo.get_all()

        return {"users": users}

    async def get_by_id(self, id: int) -> dict:
        user = await self.repo.get(id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return {"user": user}

    async def delete(self, id: int) -> dict:
        user = await self.repo.delete(id)
        return {"status": True, "deleted": user}

    async def login(self, body: UserLogin):
        user = await self.repo.get_by_email(body.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        hashed_password = self._create_hash(body.password)
        if compare_digest(hashed_password, user.password):
            jwt = encode_token({"id": user.id, "email": user.email})
            return {"status": True, "access_token": jwt}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    async def register(self, body: RegisterUser) -> dict:
        hashed_password = self._create_hash(body.password)
        user = RegisterUser(email=body.email, password=hashed_password)
        try:
            result = await self.repo.create(user)
            return {"status": True, "user_id": result}
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
