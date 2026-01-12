from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Enrollment.models.enrollment import Enrollment

class EnrollmentRepository:
    async def create(self, data: dict, session: AsyncSession):
        enrollment = Enrollment(**data)
        session.add(enrollment)
        await session.commit()
        await session.refresh(enrollment)
        return enrollment

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Enrollment).options(
                selectinload(Enrollment.student),
                selectinload(Enrollment.group)
            )
        )
        return result.scalars().all()

    async def get_by_id(self, enrollment_id: int, session: AsyncSession):
        return await session.get(
            Enrollment,
            enrollment_id,
            options=[selectinload(Enrollment.student), selectinload(Enrollment.group)]
        )

    async def update(self, enrollment_id: int, data: dict, session: AsyncSession):
        enrollment = await self.get_by_id(enrollment_id, session)
        if not enrollment:
            return None

        for key, value in data.items():
            if value is not None and hasattr(enrollment, key):
                if key in {"student_id", "group_id"}:
                    continue
                setattr(enrollment, key, value)

        await session.commit()
        await session.refresh(enrollment)
        return enrollment

    async def delete(self, enrollment_id: int, session: AsyncSession):
        enrollment = await self.get_by_id(enrollment_id, session)
        if not enrollment:
            return None
        await session.delete(enrollment)
        await session.commit()
        return enrollment