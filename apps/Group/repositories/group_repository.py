from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Group.models.group import Group

class GroupRepository:
    async def create(self, data: dict, session: AsyncSession):
        group = Group(**data)
        session.add(group)
        await session.commit()
        await session.refresh(group)
        return group

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Group).options(
                selectinload(Group.course),
                selectinload(Group.teacher),
                selectinload(Group.enrollments),
                selectinload(Group.lessons),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, group_id: int, session: AsyncSession):
        return await session.get(
            Group,
            group_id,
            options=[
                selectinload(Group.course),
                selectinload(Group.teacher),
                selectinload(Group.enrollments),
                selectinload(Group.lessons),
            ]
        )

    async def update(self, group_id: int, data: dict, session: AsyncSession):
        group = await self.get_by_id(group_id, session)
        if not group:
            return None

        for key, value in data.items():
            if value is not None and hasattr(group, key):
                if key in {"course_id", "teacher_id"}:
                    continue
                setattr(group, key, value)

        await session.commit()
        await session.refresh(group)
        return group

    async def delete(self, group_id: int, session: AsyncSession):
        group = await self.get_by_id(group_id, session)
        if not group:
            return None
        await session.delete(group)
        await session.commit()
        return group