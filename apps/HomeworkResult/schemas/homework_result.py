from pydantic import BaseModel
from typing import Optional

class HomeworkResultCreate(BaseModel):
    grade: str
    comments: Optional[str] = None
    student_id: int
    homework_id: int


class HomeworkResultUpdate(BaseModel):
    grade: Optional[str] = None
    comments: Optional[str] = None


class HomeworkResultOut(BaseModel):
    id: int
    grade: str
    comments: Optional[str] = None
    student_id: int
    homework_id: int

    class Config:
        from_attributes = True