from pydantic import BaseModel
from datetime import date
from typing import Optional

class HomeworkCreate(BaseModel):
    description: str
    due_date: date
    lesson_id: int


class HomeworkUpdate(BaseModel):
    description: Optional[str] = None
    due_date: Optional[date] = None


class HomeworkOut(BaseModel):
    id: int
    description: str
    due_date: date
    lesson_id: int

    class Config:
        from_attributes = True