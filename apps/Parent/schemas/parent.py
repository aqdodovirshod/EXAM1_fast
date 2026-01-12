from pydantic import BaseModel, EmailStr
from typing import Optional


class ParentCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    user_id: int


class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None  


class ParentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr   
    user_id: int

    class Config:
        from_attributes = True