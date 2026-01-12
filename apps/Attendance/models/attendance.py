from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, Date
from datetime import date
from core.config.database import BaseModel
from apps.Student.models.student import Student
from apps.Lesson.models.lesson import Lesson

class Attendance(BaseModel):
    __tablename__ = "attendances"   

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), index=True)

    student: Mapped["Student"] = relationship(back_populates="attendances")
    lesson: Mapped["Lesson"] = relationship(back_populates="attendances")