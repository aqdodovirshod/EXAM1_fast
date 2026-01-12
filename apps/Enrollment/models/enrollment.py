from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, String, ForeignKey
from datetime import date
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Student.models.student import Student
    from apps.Group.models.group import Group

class Enrollment(BaseModel):
    __tablename__ = "enrollments"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    enroll_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), index=True)

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    group: Mapped["Group"] = relationship(back_populates="enrollments")