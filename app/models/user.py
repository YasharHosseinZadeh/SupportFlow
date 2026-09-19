from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.ticket import Ticket
    from app.models.comment import Comment


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(String(100))

    email : Mapped[str] = mapped_column(String(225),unique=True)

    password_hash : Mapped[str] = mapped_column(String(255))

    role : Mapped[str] = mapped_column(String(20),default="customer")

    tickets : Mapped[list["Ticket"]] = relationship(back_populates = "customer")

    comments : Mapped[list["Comment"]] = relationship(back_populates = "author")
