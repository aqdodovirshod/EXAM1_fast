from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.config.database import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.User.models.user import User

class Role(BaseModel):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan"
    )