from .schemas import User, RegisterUser
from typing import List


class UsersRepository:
    def __init__(self, db):
        self.db = db

    async def get(self, id: int) -> User | None:
        user = await self.db.fetchrow("SELECT * FROM users WHERE id=$1", id)
        if not user:
            return None

        user = dict(user)
        result = User(
            id=id,
            email=user.get("email"),
            password=user.get("password"),
            created_at=user.get("created_at"),
        )
        return result

    async def get_all(self) -> List[User]:
        records = await self.db.fetch("SELECT * FROM users")
        users = [dict(record) for record in records]
        users = [
            User(
                id=user.get("id"),
                email=user.get("email"),
                created_at=user.get("created_at"),
            )
            for user in users
        ]
        return users

    async def delete(self, id: int) -> User | None:
        user = self.db.fetchrow("DELETE FROM users WHERE id=$1", id)
        if not user:
            return None

        user = dict(user)
        result = User(
            id=user.get("id"),
            email=user.get("email"),
            created_at=user.get("created_at"),
        )
        return result

    async def create(self, u: RegisterUser) -> int:
        """Creates user with data from u. Returns new user id."""
        new_user_id = await self.db.fetchval(
            "INSERT INTO users (email, password) VALUES($1, $2) RETURNING id",
            u.email,
            u.password,
        )
        return new_user_id
