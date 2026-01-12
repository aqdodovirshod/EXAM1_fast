from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from apps.Lesson.repositories.lesson_repository import LessonRepository
from apps.Group.models.group import Group
from apps.Lesson.schemas.lesson import LessonCreate, LessonUpdate, LessonOut

class LessonService:
    def __init__(self):
        self.repo = LessonRepository()

    async def create_lesson(self, data: LessonCreate, session: AsyncSession):
        group = await session.get(Group, data.group_id)
        if not group:
            raise HTTPException(status_code=400, detail="Group not found")

        if data.end_time <= data.start_time:
            raise HTTPException(status_code=400, detail="end_time must be after start_time")

        lesson = await self.repo.create(data.dict(), session)

        return LessonOut(
            id=lesson.id,
            lesson_date=lesson.lesson_date,
            start_time=lesson.start_time,
            end_time=lesson.end_time,
            topic=lesson.topic,
            group_id=lesson.group_id,
        )

    async def get_lessons(self, session: AsyncSession):
        lessons = await self.repo.get_all(session)
        return [
            LessonOut(
                id=l.id,
                lesson_date=l.lesson_date,
                start_time=l.start_time,
                end_time=l.end_time,
                topic=l.topic,
                group_id=l.group_id,
            )
            for l in lessons
        ]

    async def get_lesson(self, lesson_id: int, session: AsyncSession):
        lesson = await self.repo.get_by_id(lesson_id, session)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        return LessonOut(
            id=lesson.id,
            lesson_date=lesson.lesson_date,
            start_time=lesson.start_time,
            end_time=lesson.end_time,
            topic=lesson.topic,
            group_id=lesson.group_id,
        )

    async def update_lesson(self, lesson_id: int, data: LessonUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"group_id"})
        lesson = await self.repo.update(lesson_id, update_data, session)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        return LessonOut(
            id=lesson.id,
            lesson_date=lesson.lesson_date,
            start_time=lesson.start_time,
            end_time=lesson.end_time,
            topic=lesson.topic,
            group_id=lesson.group_id,
        )

    async def delete_lesson(self, lesson_id: int, session: AsyncSession):
        lesson = await self.repo.delete(lesson_id, session)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson