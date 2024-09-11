from .config import Config
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Member(Config.BASE):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]

    group: Mapped["Group"] = relationship(back_populates="member")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    # role: Mapped["Role"] = relationship(back_populates="member")
    # role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    lesson_members: Mapped[List["LessonMember"]] = relationship(back_populates="member")


# + name: str
# + telegram_id: int
# + role_id: int
# + group_id: int
