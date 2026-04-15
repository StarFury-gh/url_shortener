from .schemas import User, RegisterUser
from typing import List


class UsersRepository:
    def __init__(self, db):
        self.db = db

    async def get(self, id: int, include_password=False) -> User | None:
        stmt = f"SELECT id, email, created_at{', password' if include_password else ''} FROM users WHERE id=$1"

        print(stmt)

        user = await self.db.fetchrow(stmt, id)
        if not user:
            return None

        user = dict(user)

        result = User(
            id=id,
            password=user.get("password"),
            email=user.get("email"),
            created_at=user.get("created_at"),
        )

        return result.model_dump(exclude_none=True)

    async def get_all(self) -> List[User]:
        records = await self.db.fetch("SELECT id, email, created_at FROM users")
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

    async def get_by_email(self, email: str) -> User:
        record = await self.db.fetchrow(
            "SELECT id, email, password FROM users WHERE email=$1", email
        )
        if record is None:
            return None

        record = dict(record)
        user = User(
            id=record.get("id"),
            email=record.get("email"),
            password=record.get("password"),
        )

        return user

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
