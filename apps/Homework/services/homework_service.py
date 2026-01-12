from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from apps.Homework.repositories.homework_repository import HomeworkRepository
from apps.Lesson.models.lesson import Lesson
from apps.Homework.schemas.homework import HomeworkCreate, HomeworkUpdate, HomeworkOut

class HomeworkService:
    def __init__(self):
        self.repo = HomeworkRepository()

    async def create_homework(self, data: HomeworkCreate, session: AsyncSession):
        lesson = await session.get(Lesson, data.lesson_id)
        if not lesson:
            raise HTTPException(status_code=400, detail="Lesson not found")

        homework = await self.repo.create(data.dict(), session)

        return HomeworkOut(
            id=homework.id,
            description=homework.description,
            due_date=homework.due_date,
            lesson_id=homework.lesson_id,
        )

    async def get_homeworks(self, session: AsyncSession):
        homeworks = await self.repo.get_all(session)
        return [
            HomeworkOut(
                id=h.id,
                description=h.description,
                due_date=h.due_date,
                lesson_id=h.lesson_id,
            )
            for h in homeworks
        ]

    async def get_homework(self, homework_id: int, session: AsyncSession):
        homework = await self.repo.get_by_id(homework_id, session)
        if not homework:
            raise HTTPException(status_code=404, detail="Homework not found")

        return HomeworkOut(
            id=homework.id,
            description=homework.description,
            due_date=homework.due_date,
            lesson_id=homework.lesson_id,
        )

    async def update_homework(self, homework_id: int, data: HomeworkUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"lesson_id"})
        homework = await self.repo.update(homework_id, update_data, session)
        if not homework:
            raise HTTPException(status_code=404, detail="Homework not found")

        return HomeworkOut(
            id=homework.id,
            description=homework.description,
            due_date=homework.due_date,
            lesson_id=homework.lesson_id,
        )

    async def delete_homework(self, homework_id: int, session: AsyncSession):
        homework = await self.repo.delete(homework_id, session)
        if not homework:
            raise HTTPException(status_code=404, detail="Homework not found")
        return homework