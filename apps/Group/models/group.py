from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from datetime import date
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Lesson.models.lesson import Lesson
    from apps.Teacher.models.teacher import Teacher
    from apps.Course.models.course import Course
    from apps.Enrollment.models.enrollment import Enrollment

class Group(BaseModel):
    __tablename__ = "groups"   

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    max_students: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), index=True)

    course: Mapped["Course"] = relationship(back_populates="groups")
    teacher: Mapped["Teacher"] = relationship(back_populates="groups")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="group")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="group")