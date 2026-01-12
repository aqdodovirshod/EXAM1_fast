from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Teacher.models.teacher import Teacher

class TeacherRepository:
    async def create(self, data: dict, session: AsyncSession):
        teacher = Teacher(**data)
        session.add(teacher)
        await session.commit()
        await session.refresh(teacher)
        return teacher

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Teacher).options(selectinload(Teacher.user))
        )
        return result.scalars().all()

    async def get_by_id(self, teacher_id: int, session: AsyncSession):
        return await session.get(Teacher, teacher_id, options=[selectinload(Teacher.user)])

    async def update(self, teacher_id: int, data: dict, session: AsyncSession):
        teacher = await self.get_by_id(teacher_id, session)
        if not teacher:
            return None

        if "user_id" in data:
            data.pop("user_id")

        for key, value in data.items():
            if value is not None and hasattr(teacher, key):
                setattr(teacher, key, value)

        await session.commit()
        await session.refresh(teacher)
        return teacher

    async def delete(self, teacher_id: int, session: AsyncSession):
        teacher = await self.get_by_id(teacher_id, session)
        if not teacher:
            return None
        await session.delete(teacher)
        await session.commit()
        return teacher