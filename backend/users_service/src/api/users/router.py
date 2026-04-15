from fastapi import APIRouter, Depends, Query

from core.security import require_admin

from .schemas import UserLogin, RegisterUser, GetUsersResponse
from .dependencies import get_service
from .service import UsersService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=GetUsersResponse)
async def get_all_users(service: UsersService = Depends(get_service)):
    return await service.get_all()


@users_router.get("/{id}")
async def get_user_by_id(id: int, service: UsersService = Depends(get_service)):
    return await service.get_by_id(id)


@users_router.post("/login")
async def login_user(body: UserLogin, service: UsersService = Depends(get_service)):
    return await service.login(body)


@users_router.post("/register")
async def register_user(
    body: RegisterUser, service: UsersService = Depends(get_service)
):
    return await service.register(body)


@users_router.delete("/delete")
async def delete_user(id: int = Query(...), admin=Depends(require_admin)):
    return f"Should delete user #{id}"
