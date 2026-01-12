from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select

from apps.Parent.repositories.parent_repository import ParentRepository
from apps.Parent.models.parent import Parent
from apps.User.models.user import User
from apps.Role.models.role import Role
from apps.Parent.schemas.parent import ParentCreate, ParentUpdate, ParentOut


class ParentService:
    def __init__(self):
        self.repo = ParentRepository()

    async def create_parent(self, data: ParentCreate, session: AsyncSession):
        user = await session.get(User, data.user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        if user.email != data.email:
            raise HTTPException(status_code=400, detail="Email mismatch with user")

        role = await session.get(Role, user.role_id)
        if not role or role.name.lower() != "parent":
            raise HTTPException(status_code=400, detail="User must have 'parent' role")

        existing = await session.execute(select(Parent).where(Parent.user_id == data.user_id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Parent already exists for this user")

        parent = await self.repo.create(data.dict(exclude={"email"}), session)
    
        await session.refresh(user)

        return ParentOut(
            id=parent.id,
            first_name=parent.first_name,
            last_name=parent.last_name,
            phone=parent.phone,
            email=user.email,
            user_id=parent.user_id
        )

    async def get_parents(self, session: AsyncSession):
        parents = await self.repo.get_all(session)
        return [
            ParentOut(
                id=p.id,
                first_name=p.first_name,
                last_name=p.last_name,
                phone=p.phone,
                email=p.user.email,
                user_id=p.user_id
            )
            for p in parents
        ]

    async def get_parent(self, parent_id: int, session: AsyncSession):
        parent = await self.repo.get_by_id(parent_id, session)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")

        return ParentOut(
            id=parent.id,
            first_name=parent.first_name,
            last_name=parent.last_name,
            phone=parent.phone,
            email=parent.user.email,
            user_id=parent.user_id
        )

    async def update_parent(self, parent_id: int, data: ParentUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"email", "user_id"})
        parent = await self.repo.update(parent_id, update_data, session)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")

        return ParentOut(
            id=parent.id,
            first_name=parent.first_name,
            last_name=parent.last_name,
            phone=parent.phone,
            email=parent.user.email,
            user_id=parent.user_id
        )

    async def delete_parent(self, parent_id: int, session: AsyncSession):
        parent = await self.repo.delete(parent_id, session)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        return parent