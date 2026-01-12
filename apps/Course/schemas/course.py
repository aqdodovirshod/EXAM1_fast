from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_month: float  


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_month: Optional[float] = None   


class CourseOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price_per_month: float

    class Config:
        from_attributes = True