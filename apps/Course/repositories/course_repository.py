from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Course.models.course import Course

class CourseRepository:
    async def create(self, data: dict, session: AsyncSession):
        course = Course(**data)
        session.add(course)
        await session.commit()
        await session.refresh(course)
        return course

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Course).options(
                selectinload(Course.groups)
            )
        )
        return result.scalars().all()

    async def get_by_id(self, course_id: int, session: AsyncSession):
        return await session.get(
            Course,
            course_id,
            options=[selectinload(Course.groups)]
        )

    async def update(self, course_id: int, data: dict, session: AsyncSession):
        course = await self.get_by_id(course_id, session)
        if not course:
            return None

        for key, value in data.items():
            if value is not None and hasattr(course, key):
                setattr(course, key, value)

        await session.commit()
        await session.refresh(course)
        return course

    async def delete(self, course_id: int, session: AsyncSession):
        course = await self.get_by_id(course_id, session)
        if not course:
            return None
        await session.delete(course)
        await session.commit()
        return course