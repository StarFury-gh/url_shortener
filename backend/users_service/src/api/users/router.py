from fastapi import APIRouter, Depends
from .schemas import UserLogin, RegisterUser, GetUsersResponse

from .dependencies import get_service
from .service import UsersService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=GetUsersResponse)
async def get_all_users(service: UsersService = Depends(get_service)):
    return await service.get_all()


@users_router.get("/{id}")
async def get_user_by_id(id: int):
    return f"Should return user with id #{id}"


@users_router.post("/login")
async def login_user(body: UserLogin):
    return "Should return JWT or an Error after login user"


@users_router.post("/register")
async def register_user(
    body: RegisterUser, service: UsersService = Depends(get_service)
):
    return await service.register(body)
