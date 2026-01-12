from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from apps.Teacher.repositories.teacher_repository import TeacherRepository
from apps.Teacher.models.teacher import Teacher
from apps.User.models.user import User
from apps.Role.models.role import Role
from apps.Teacher.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherOut

class TeacherService:
    def __init__(self):
        self.repo = TeacherRepository()

    async def create_teacher(self, data: TeacherCreate, session: AsyncSession):
        user = await session.get(User, data.user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        if user.email != data.email:
            raise HTTPException(status_code=400, detail="Email mismatch with user")

        role = await session.get(Role, user.role_id)
        if not role or role.name.lower() != "teacher":
            raise HTTPException(status_code=400, detail="User must have 'teacher' role")

        existing = await session.execute(select(Teacher).where(Teacher.user_id == data.user_id))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Teacher already exists for this user")

        teacher = await self.repo.create(data.dict(exclude={"email"}), session)

        await session.refresh(user)
        
        return TeacherOut(
            id=teacher.id,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            phone=teacher.phone,
            email=user.email,
            user_id=teacher.user_id
        )

    async def get_teachers(self, session: AsyncSession):
        teachers = await self.repo.get_all(session)
        return [
            TeacherOut(
                id=t.id,
                first_name=t.first_name,
                last_name=t.last_name,
                phone=t.phone,
                email=t.user.email,
                user_id=t.user_id
            )
            for t in teachers
        ]

    async def get_teacher(self, teacher_id: int, session: AsyncSession):
        teacher = await self.repo.get_by_id(teacher_id, session)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        return TeacherOut(
            id=teacher.id,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            phone=teacher.phone,
            email=teacher.user.email,
            user_id=teacher.user_id
        )

    async def update_teacher(self, teacher_id: int, data: TeacherUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"email", "user_id"})
        teacher = await self.repo.update(teacher_id, update_data, session)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        return TeacherOut(
            id=teacher.id,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            phone=teacher.phone,
            email=teacher.user.email,
            user_id=teacher.user_id
        )

    async def delete_teacher(self, teacher_id: int, session: AsyncSession):
        teacher = await self.repo.delete(teacher_id, session)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return teacher