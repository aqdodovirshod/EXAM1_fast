from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, Float, ForeignKey, String
from datetime import date
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Student.models.student import Student
    from apps.Parent.models.parent import Parent

class Payment(BaseModel):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="completed")

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"), index=True)

    student: Mapped["Student"] = relationship(back_populates="payments")
    parent: Mapped["Parent"] = relationship(back_populates="payments")