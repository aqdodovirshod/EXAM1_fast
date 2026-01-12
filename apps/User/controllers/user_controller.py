from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_session
from apps.User.schemas.user_schema import UserOut, UserRegister, UserLogin
from apps.User.schemas.token_schema import Token
from apps.User.services.user_service import UserService
from apps.User.services.user_dependency import get_current_user
from apps.User.services.permission import admin_required
from apps.User.models.user import User

user_router = APIRouter(prefix="/auth", tags=["auth"])

@user_router.post("/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, session: AsyncSession = Depends(get_session)):
    return await UserService.register_user(data=data, session=session)

@user_router.post("/login/", response_model=Token)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await UserService.login_user(data=data, session=session)
    return Token(access_token=result["access_token"], token_type="bearer")

@user_router.get("/me/", response_model=UserOut)
async def profile(user: User = Depends(get_current_user)):
    return user

@user_router.get("/admin/", response_model=UserOut)
async def admin_profile(user: User = Depends(admin_required)):
    return user