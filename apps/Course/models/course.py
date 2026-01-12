from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Float
from core.config.database import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.Group.models.group import Group

class Course(BaseModel):
    __tablename__ = "courses"  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price_per_month: Mapped[float] = mapped_column(Float, nullable=False)

    groups: Mapped[list["Group"]] = relationship(back_populates="course")