from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, Time, ForeignKey, Text
from datetime import date, time
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.Group.models.group import Group
    from apps.Homework.models.homework import Homework
    from apps.Attendance.models.attendance import Attendance

class Lesson(BaseModel):
    __tablename__ = "lessons"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    topic: Mapped[str] = mapped_column(Text, nullable=False)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), index=True)

    group: Mapped["Group"] = relationship(back_populates="lessons")
    homeworks: Mapped[list["Homework"]] = relationship(back_populates="lesson")
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="lesson")