from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from apps.Group.repositories.group_repository import GroupRepository
from apps.Group.models.group import Group
from apps.Course.models.course import Course
from apps.Teacher.models.teacher import Teacher
from apps.Group.schemas.group import GroupCreate, GroupUpdate, GroupOut

class GroupService:
    def __init__(self):
        self.repo = GroupRepository()

    async def create_group(self, data: GroupCreate, session: AsyncSession):
        existing = await session.execute(select(Group).where(Group.name == data.name))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Group with this name already exists")

        if data.end_date < data.start_date:
            raise HTTPException(status_code=400, detail="end_date must be after start_date")

        course = await session.get(Course, data.course_id)
        if not course:
            raise HTTPException(status_code=400, detail="Course not found")

        teacher = await session.get(Teacher, data.teacher_id)
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found")

        group = await self.repo.create(data.dict(), session)

        return GroupOut(
            id=group.id,
            name=group.name,
            max_students=group.max_students,
            start_date=group.start_date,
            end_date=group.end_date,
            course_id=group.course_id,
            teacher_id=group.teacher_id,
        )

    async def get_groups(self, session: AsyncSession):
        groups = await self.repo.get_all(session)
        return [
            GroupOut(
                id=g.id,
                name=g.name,
                max_students=g.max_students,
                start_date=g.start_date,
                end_date=g.end_date,
                course_id=g.course_id,
                teacher_id=g.teacher_id,
            )
            for g in groups
        ]

    async def get_group(self, group_id: int, session: AsyncSession):
        group = await self.repo.get_by_id(group_id, session)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        return GroupOut(
            id=group.id,
            name=group.name,
            max_students=group.max_students,
            start_date=group.start_date,
            end_date=group.end_date,
            course_id=group.course_id,
            teacher_id=group.teacher_id,
        )

    async def update_group(self, group_id: int, data: GroupUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"course_id", "teacher_id"})
        group = await self.repo.update(group_id, update_data, session)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        return GroupOut(
            id=group.id,
            name=group.name,
            max_students=group.max_students,
            start_date=group.start_date,
            end_date=group.end_date,
            course_id=group.course_id,
            teacher_id=group.teacher_id,
        )

    async def delete_group(self, group_id: int, session: AsyncSession):
        group = await self.repo.delete(group_id, session)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group