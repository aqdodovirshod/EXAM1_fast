from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from datetime import timedelta

from apps.User.models.user import User
from apps.Role.models.role import Role
from apps.User.schemas.user_schema import UserRegister, UserLogin
from apps.User.services.auth_service import (
    verify_password, hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)

class UserService:

    @staticmethod
    async def register_user(data: UserRegister, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists")

        result = await session.execute(select(User).where(User.username == data.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this username already exists")

        result = await session.execute(select(Role).where(Role.id == data.role_id))
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role_id")

        new_user = User(
            username=data.username,
            email=data.email,
            role_id=role.id,
            password=hash_password(data.password)
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def login_user(data: UserLogin, session: AsyncSession):
        result = await session.execute(
            select(User).options(selectinload(User.role)).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            {"sub": user.email, "user_id": user.id, "role": user.role.name},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user}

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(
            select(User).options(selectinload(User.role)).where(User.email == email)
        )
        return result.scalar_one_or_none()