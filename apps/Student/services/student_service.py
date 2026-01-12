from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apps.Student.repositories.student_repository import StudentRepository
from apps.Student.models.student import Student
from apps.Student.schemas.student import StudentCreate, StudentUpdate
from apps.User.models.user import User
from apps.Role.models.role import Role


class StudentService:
    def __init__(self):
        self.repo = StudentRepository()

    async def create_student(self, data: StudentCreate, session: AsyncSession):
        user = await session.get(User, data.user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        if user.email != data.email:
            raise HTTPException(status_code=400, detail="Email mismatch with user")

        role = await session.get(Role, user.role_id)
        if not role or role.name.lower() != "student":
            raise HTTPException(status_code=400, detail="User must have 'student' role")

        existing = await session.execute(select(Student).where(Student.user_id == data.user_id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Student already exists for this user")

        return await self.repo.create(data.dict(exclude={"email"}), session)

    async def get_students(self, session: AsyncSession):
        result = await session.execute(
            select(Student).options(selectinload(Student.user))
        )
        return result.scalars().all()

    async def get_student(self, student_id: int, session: AsyncSession):
        student = await session.get(Student, student_id, options=[selectinload(Student.user)])
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    async def update_student(self, student_id: int, data: StudentUpdate, session: AsyncSession):
        student = await self.repo.update(student_id, data.dict(exclude_unset=True, exclude={"email"}), session)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    async def delete_student(self, student_id: int, session: AsyncSession):
        student = await self.repo.delete(student_id, session)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student