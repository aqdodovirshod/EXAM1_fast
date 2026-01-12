from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Student.models.student import Student
    from apps.Homework.models.homework import Homework

class HomeworkResult(BaseModel):
    __tablename__ = "homework_results"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    grade: Mapped[str] = mapped_column(String(50), nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    homework_id: Mapped[int] = mapped_column(ForeignKey("homeworks.id"), index=True)

    student: Mapped["Student"] = relationship(back_populates="homework_results")
    homework: Mapped["Homework"] = relationship(back_populates="results")