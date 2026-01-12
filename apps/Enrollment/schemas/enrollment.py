from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

class EnrollmentCreate(BaseModel):
    enroll_date: date
    status: Literal["active", "completed", "dropped"] = "active"
    student_id: int
    group_id: int


class EnrollmentUpdate(BaseModel):
    enroll_date: Optional[date] = None
    status: Optional[Literal["active", "completed", "dropped"]] = None


class EnrollmentOut(BaseModel):
    id: int
    enroll_date: date
    status: str
    student_id: int
    group_id: int

    class Config:
        from_attributes = True