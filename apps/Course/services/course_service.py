from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from apps.Course.repositories.course_repository import CourseRepository
from apps.Course.models.course import Course
from apps.Course.schemas.course import CourseCreate, CourseUpdate, CourseOut

class CourseService:
    def __init__(self):
        self.repo = CourseRepository()

    async def create_course(self, data: CourseCreate, session: AsyncSession):
        existing = await session.execute(select(Course).where(Course.name == data.name))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Course with this name already exists")

        course = await self.repo.create(data.dict(), session)

        return CourseOut(
            id=course.id,
            name=course.name,
            description=course.description,
            price_per_month=course.price_per_month,
        )

    async def get_courses(self, session: AsyncSession):
        courses = await self.repo.get_all(session)
        return [
            CourseOut(
                id=c.id,
                name=c.name,
                description=c.description,
                price_per_month=c.price_per_month,
            )
            for c in courses
        ]

    async def get_course(self, course_id: int, session: AsyncSession):
        course = await self.repo.get_by_id(course_id, session)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return CourseOut(
            id=course.id,
            name=course.name,
            description=course.description,
            price_per_month=course.price_per_month,
        )

    async def update_course(self, course_id: int, data: CourseUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True)
        course = await self.repo.update(course_id, update_data, session)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return CourseOut(
            id=course.id,
            name=course.name,
            description=course.description,
            price_per_month=course.price_per_month,
        )

    async def delete_course(self, course_id: int, session: AsyncSession):
        course = await self.repo.delete(course_id, session)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course