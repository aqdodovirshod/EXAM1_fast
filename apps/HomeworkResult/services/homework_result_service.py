from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from apps.HomeworkResult.repositories.homework_result_repository import HomeworkResultRepository
from apps.HomeworkResult.models.homework_result import HomeworkResult
from apps.Student.models.student import Student
from apps.Homework.models.homework import Homework
from apps.HomeworkResult.schemas.homework_result import HomeworkResultCreate, HomeworkResultUpdate, HomeworkResultOut

class HomeworkResultService:
    def __init__(self):
        self.repo = HomeworkResultRepository()

    async def create_homework_result(self, data: HomeworkResultCreate, session: AsyncSession):
        student = await session.get(Student, data.student_id)
        if not student:
            raise HTTPException(status_code=400, detail="Student not found")

        homework = await session.get(Homework, data.homework_id)
        if not homework:
            raise HTTPException(status_code=400, detail="Homework not found")

        existing = await session.execute(
            select(HomeworkResult).where(
                HomeworkResult.student_id == data.student_id,
                HomeworkResult.homework_id == data.homework_id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Result for this homework already exists")

        result = await self.repo.create(data.dict(), session)

        return HomeworkResultOut(
            id=result.id,
            grade=result.grade,
            comments=result.comments,
            student_id=result.student_id,
            homework_id=result.homework_id,
        )

    async def get_homework_results(self, session: AsyncSession):
        results = await self.repo.get_all(session)
        return [
            HomeworkResultOut(
                id=r.id,
                grade=r.grade,
                comments=r.comments,
                student_id=r.student_id,
                homework_id=r.homework_id,
            )
            for r in results
        ]

    async def get_homework_result(self, result_id: int, session: AsyncSession):
        result = await self.repo.get_by_id(result_id, session)
        if not result:
            raise HTTPException(status_code=404, detail="Homework result not found")

        return HomeworkResultOut(
            id=result.id,
            grade=result.grade,
            comments=result.comments,
            student_id=result.student_id,
            homework_id=result.homework_id,
        )

    async def update_homework_result(self, result_id: int, data: HomeworkResultUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True)
        result = await self.repo.update(result_id, update_data, session)
        if not result:
            raise HTTPException(status_code=404, detail="Homework result not found")

        return HomeworkResultOut(
            id=result.id,
            grade=result.grade,
            comments=result.comments,
            student_id=result.student_id,
            homework_id=result.homework_id,
        )

    async def delete_homework_result(self, result_id: int, session: AsyncSession):
        result = await self.repo.delete(result_id, session)
        if not result:
            raise HTTPException(status_code=404, detail="Homework result not found")
        return result