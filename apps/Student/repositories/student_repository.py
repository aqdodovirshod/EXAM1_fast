from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from apps.Student.models.student import Student
from apps.User.models.user import User
from apps.Role.models.role import Role

class StudentRepository:
    async def create(self, data: dict, session: AsyncSession):
        user = await session.get(User, data.get("user_id"))
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        role = await session.get(Role, user.role_id)
        if not role or role.name.lower() != "student":
            raise HTTPException(status_code=400, detail="User must have 'student' role")

        student = Student(**data)
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student

    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(Student))
        return result.scalars().all()

    async def get_by_id(self, student_id: int, session: AsyncSession):
        student = await session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    async def update(self, student_id: int, data: dict, session: AsyncSession):
        student = await self.get_by_id(student_id, session)
        for key, value in data.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)
        await session.commit()
        await session.refresh(student)
        return student

    async def delete(self, student_id: int, session: AsyncSession):
        student = await self.get_by_id(student_id, session)
        await session.delete(student)
        await session.commit()
        return student