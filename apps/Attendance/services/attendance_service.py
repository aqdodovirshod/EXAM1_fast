from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from apps.Attendance.repositories.attendance_repository import AttendanceRepository
from apps.Student.models.student import Student
from apps.Lesson.models.lesson import Lesson
from apps.Attendance.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut

class AttendanceService:
    def __init__(self):
        self.repo = AttendanceRepository()

    async def create_attendance(self, data: AttendanceCreate, session: AsyncSession):
        student = await session.get(Student, data.student_id)
        if not student:
            raise HTTPException(status_code=400, detail="Student not found")

        lesson = await session.get(Lesson, data.lesson_id)
        if not lesson:
            raise HTTPException(status_code=400, detail="Lesson not found")

        attendance = await self.repo.create(data.dict(), session)

        return AttendanceOut(
            id=attendance.id,
            attendance_date=attendance.attendance_date,
            status=attendance.status,
            student_id=attendance.student_id,
            lesson_id=attendance.lesson_id,
        )

    async def get_attendances(self, session: AsyncSession):
        attendances = await self.repo.get_all(session)
        return [
            AttendanceOut(
                id=a.id,
                attendance_date=a.attendance_date,
                status=a.status,
                student_id=a.student_id,
                lesson_id=a.lesson_id,
            )
            for a in attendances
        ]

    async def get_attendance(self, attendance_id: int, session: AsyncSession):
        attendance = await self.repo.get_by_id(attendance_id, session)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance not found")

        return AttendanceOut(
            id=attendance.id,
            attendance_date=attendance.attendance_date,
            status=attendance.status,
            student_id=attendance.student_id,
            lesson_id=attendance.lesson_id,
        )

    async def update_attendance(self, attendance_id: int, data: AttendanceUpdate, session: AsyncSession):
        update_data = data.dict(exclude_unset=True, exclude={"student_id", "lesson_id"})
        attendance = await self.repo.update(attendance_id, update_data, session)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance not found")

        return AttendanceOut(
            id=attendance.id,
            attendance_date=attendance.attendance_date,
            status=attendance.status,
            student_id=attendance.student_id,
            lesson_id=attendance.lesson_id,
        )

    async def delete_attendance(self, attendance_id: int, session: AsyncSession):
        attendance = await self.repo.delete(attendance_id, session)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance not found")
        return attendance