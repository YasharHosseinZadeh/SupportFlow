from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.ticket import Ticket
    from models.user import User


class Comment(Base):
    __tablename__ = "comments"

    id : Mapped[int] = mapped_column(primary_key=True)

    content : Mapped[str] = mapped_column(String(255))

    ticket_id : Mapped[int] = mapped_column(ForeignKey("tickets.id"))

    author_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    ticket : Mapped["Ticket"] = relationship(back_populates = "comments")

    author : Mapped["User"] = relationship(back_populates = "comments")