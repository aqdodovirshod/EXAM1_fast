from pydantic import BaseModel, EmailStr
from typing import Optional

class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr  
    user_id: int

class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None  

class TeacherOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr  
    user_id: int

    class Config:
        from_attributes = True