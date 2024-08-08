from .config import Config
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Member(Config.BASE):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]

    role: Mapped["Role"] = relationship()
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    group: Mapped["Group"] = relationship(back_populates="students")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))


# + name: str
# + telegram_id: int
# + role_id: int
# + group_id: int
