from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Lesson.models.lesson import Lesson

class LessonRepository:
    async def create(self, data: dict, session: AsyncSession):
        lesson = Lesson(**data)
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)
        return lesson

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Lesson).options(
                selectinload(Lesson.group),
                selectinload(Lesson.homeworks),
                selectinload(Lesson.attendances),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, lesson_id: int, session: AsyncSession):
        return await session.get(
            Lesson,
            lesson_id,
            options=[
                selectinload(Lesson.group),
                selectinload(Lesson.homeworks),
                selectinload(Lesson.attendances),
            ]
        )

    async def update(self, lesson_id: int, data: dict, session: AsyncSession):
        lesson = await self.get_by_id(lesson_id, session)
        if not lesson:
            return None

        for key, value in data.items():
            if value is not None and hasattr(lesson, key):
                if key == "group_id":
                    continue
                setattr(lesson, key, value)

        await session.commit()
        await session.refresh(lesson)
        return lesson

    async def delete(self, lesson_id: int, session: AsyncSession):
        lesson = await self.get_by_id(lesson_id, session)
        if not lesson:
            return None
        await session.delete(lesson)
        await session.commit()
        return lesson