from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from apps.Role.models.role import Role
from apps.Role.schemas.role import RoleCreate

class RoleService:

    @staticmethod
    async def create_role(data: RoleCreate, session: AsyncSession):
        result = await session.execute(select(Role).where(Role.name == data.name))
        existing_role = result.scalar_one_or_none()
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already exists")

        new_role = Role(name=data.name)
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
        return new_role

    @staticmethod
    async def get_roles(session: AsyncSession):
        result = await session.execute(select(Role))
        return result.scalars().all()