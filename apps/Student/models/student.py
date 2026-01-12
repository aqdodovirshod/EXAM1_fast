from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from datetime import date
from core.config.database import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.Parent.models.parent import Parent
    from apps.User.models.user import User
    from apps.Payment.models.payment import Payment
    from apps.Enrollment.models.enrollment import Enrollment
    from apps.HomeworkResult.models.homework_result import HomeworkResult
    from apps.Attendance.models.attendance import Attendance

class Student(BaseModel):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    date_of_birth: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String(150))
    level: Mapped[str] = mapped_column(String(150))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"))
    
    user: Mapped["User"] = relationship(back_populates="student", uselist=False)
    parent: Mapped["Parent"] = relationship(back_populates="students")
    payments: Mapped[list["Payment"]] = relationship(back_populates="student")

    homework_results: Mapped[list["HomeworkResult"]] = relationship(back_populates="student")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="student")
