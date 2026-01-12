from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.Attendance.models.attendance import Attendance

class AttendanceRepository:
    async def create(self, data: dict, session: AsyncSession):
        attendance = Attendance(**data)
        session.add(attendance)
        await session.commit()
        await session.refresh(attendance)
        return attendance

    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Attendance).options(
                selectinload(Attendance.student),
                selectinload(Attendance.lesson),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, attendance_id: int, session: AsyncSession):
        return await session.get(
            Attendance,
            attendance_id,
            options=[
                selectinload(Attendance.student),
                selectinload(Attendance.lesson),
            ]
        )

    async def update(self, attendance_id: int, data: dict, session: AsyncSession):
        attendance = await self.get_by_id(attendance_id, session)
        if not attendance:
            return None

        for key, value in data.items():
            if value is not None and hasattr(attendance, key):
                if key in {"student_id", "lesson_id"}:
                    continue
                setattr(attendance, key, value)

        await session.commit()
        await session.refresh(attendance)
        return attendance

    async def delete(self, attendance_id: int, session: AsyncSession):
        attendance = await self.get_by_id(attendance_id, session)
        if not attendance:
            return None
        await session.delete(attendance)
        await session.commit()
        return attendance