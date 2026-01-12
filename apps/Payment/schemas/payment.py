from pydantic import BaseModel, validator
from datetime import date
from typing import Optional

class PaymentCreate(BaseModel):
    amount: float
    payment_date: date
    period_start: date
    period_end: date
    student_id: int
    parent_id: int
    status: Optional[str] = "completed"

    @validator("period_end")
    def check_period(cls, v, values):
        if "period_start" in values and v < values["period_start"]:
            raise ValueError("period_end must be after period_start")
        return v


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_date: Optional[date] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    status: Optional[str] = None


class PaymentOut(BaseModel):
    id: int
    amount: float
    payment_date: date
    period_start: date
    period_end: date
    student_id: int
    parent_id: int
    status: str

    class Config:
        from_attributes = True