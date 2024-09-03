from typing import List
from .config import Config
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Group(Config.BASE):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


    member: Mapped[List["Member"]] = relationship(back_populates="group")

    topic: Mapped["Topic"] = relationship(back_populates="group")