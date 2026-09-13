from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import relationship,Mapped,mapped_column
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.comment import Comment


class Ticket(Base):
    __tablename__ = "tickets"

    id :Mapped[int] = mapped_column(primary_key=True)

    title : Mapped[str] = mapped_column(String(100))

    description : Mapped[str] = mapped_column(String(500))

    customer_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    customer : Mapped["User"] = relationship(back_populates = "tickets" )

    comments : Mapped[list["Comment"]] = relationship(back_populates = "ticket" )
