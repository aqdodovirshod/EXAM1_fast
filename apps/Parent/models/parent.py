from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import TYPE_CHECKING
from core.config.database import BaseModel

if TYPE_CHECKING:
    from apps.User.models.user import User
    from apps.Student.models.student import Student
    from apps.Payment.models.payment import Payment



class Parent(BaseModel):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(150))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="parent", uselist=False)
    students: Mapped[list["Student"]] = relationship(back_populates="parent")
    payments: Mapped[list["Payment"]] = relationship(back_populates="parent")
