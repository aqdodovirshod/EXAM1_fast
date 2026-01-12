from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceCreate(BaseModel):
    attendance_date: date
    status: str
    student_id: int
    lesson_id: int


class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None
    status: Optional[str] = None


class AttendanceOut(BaseModel):
    id: int
    attendance_date: date
    status: str
    student_id: int
    lesson_id: int

    class Config:
        from_attributes = True