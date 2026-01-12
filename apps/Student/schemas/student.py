from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, Literal
from apps.User.schemas.user_schema import UserOut

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    email: EmailStr = Field(..., max_length=150)
    level: Literal["beginner", "intermediate", "advanced"]
    parent_id: int
    user_id: int

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    level: Optional[Literal["beginner", "intermediate", "advanced"]] = None

class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    level: str
    parent_id: int
    user_id: int

    class Config:
        from_attributes = True