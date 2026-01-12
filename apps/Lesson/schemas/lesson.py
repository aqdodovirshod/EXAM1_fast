from pydantic import BaseModel, validator
from datetime import date, time
from typing import Optional

class LessonCreate(BaseModel):
    lesson_date: date
    start_time: time
    end_time: time
    topic: str
    group_id: int

    @validator("end_time")
    def check_times(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class LessonUpdate(BaseModel):
    lesson_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    topic: Optional[str] = None


class LessonOut(BaseModel):
    id: int
    lesson_date: date
    start_time: time
    end_time: time
    topic: str
    group_id: int

    class Config:
        from_attributes = True