from pydantic import BaseModel, validator
from datetime import date
from typing import Optional

class GroupCreate(BaseModel):
    name: str
    max_students: int
    start_date: date
    end_date: date
    course_id: int
    teacher_id: int

    @validator("end_date")
    def check_dates(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    max_students: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class GroupOut(BaseModel):
    id: int
    name: str
    max_students: int
    start_date: date
    end_date: date
    course_id: int
    teacher_id: int

    class Config:
        from_attributes = True