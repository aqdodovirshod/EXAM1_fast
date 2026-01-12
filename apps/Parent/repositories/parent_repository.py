from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Parent.models.parent import Parent


class ParentRepository:
    async def create(self, data: dict, session: AsyncSession):
        parent = Parent(**data)
        session.add(parent)
        await session.commit()
        await session.refresh(parent)
        return parent

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Parent).options(selectinload(Parent.user))
        )
        return result.scalars().all()

    async def get_by_id(self, parent_id: int, session: AsyncSession):
        return await session.get(Parent, parent_id, options=[selectinload(Parent.user)])

    async def update(self, parent_id: int, data: dict, session: AsyncSession):
        parent = await self.get_by_id(parent_id, session)
        if not parent:
            return None

        if "user_id" in data:
            data.pop("user_id")

        for key, value in data.items():
            if value is not None and hasattr(parent, key):
                setattr(parent, key, value)

        await session.commit()
        await session.refresh(parent)
        return parent

    async def delete(self, parent_id: int, session: AsyncSession):
        parent = await self.get_by_id(parent_id, session)
        if not parent:
            return None
        await session.delete(parent)
        await session.commit()
        return parent