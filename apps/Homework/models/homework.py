from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, ForeignKey, Text
from datetime import date
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Lesson.models.lesson import Lesson
    from apps.HomeworkResult.models.homework_result import HomeworkResult

class Homework(BaseModel):
    __tablename__ = "homeworks"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), index=True)

    lesson: Mapped["Lesson"] = relationship(back_populates="homeworks")
    results: Mapped[list["HomeworkResult"]] = relationship(back_populates="homework")