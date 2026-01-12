from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from apps.Enrollment.repositories.enrollment_repository import EnrollmentRepository
from apps.Enrollment.models.enrollment import Enrollment
from apps.Student.models.student import Student
from apps.Group.models.group import Group
from apps.Enrollment.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentOut

class EnrollmentService:
    def __init__(self):
        self.repo = EnrollmentRepository()

    async def create_enrollment(self, data: EnrollmentCreate, session: AsyncSession):
        existing = await session.execute(
            select(Enrollment).where(
                Enrollment.student_id == data.student_id,
                Enrollment.group_id == data.group_id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Student already enrolled in this group")

        student = await session.get(Student, data.student_id)
        if not student:
            raise HTTPException(status_code=400, detail="Student not found")

        group = await session.get(Group, data.group_id)
        if not group:
            raise HTTPException(status_code=400, detail="Group not found")

        enrollment = await self.repo.create(data.dict(), session)

        return EnrollmentOut(
            id=enrollment.id,
            enroll_date=enrollment.enroll_date,
            status=enrollment.status,
            student_id=enrollment.student_id,
            group_id=enrollment.group_id,
        )

    async def get_enrollments(self, session: AsyncSession):
        enrollments = await self.repo.get_all(session)
        return [
            EnrollmentOut(
                id=e.id,
                enroll_date=e.enroll_date,
                status=e.status,
                student_id=e.student_id,
                group_id=e.group_id,
            )
            for e in enrollments
        ]

    async def get_enrollment(self, enrollment_id: int, session: AsyncSession):
        enrollment = await self.repo.get_by_id(enrollment_id, session)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        return EnrollmentOut(
            id=enrollment.id,
            enroll_date=enrollment.enroll_date,
            status=enrollment.status,
            student_id=enrollment.student_id,
            group_id=enrollment.group_id,
        )

    async def update_enrollment(self, enrollment_id: int, data: EnrollmentUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"student_id", "group_id"})
        enrollment = await self.repo.update(enrollment_id, update_data, session)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        return EnrollmentOut(
            id=enrollment.id,
            enroll_date=enrollment.enroll_date,
            status=enrollment.status,
            student_id=enrollment.student_id,
            group_id=enrollment.group_id,
        )

    async def delete_enrollment(self, enrollment_id: int, session: AsyncSession):
        enrollment = await self.repo.delete(enrollment_id, session)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        return enrollment