from .config import Config
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Role(Config.BASE):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # members: Mapped[List["Member"]] = relationship(back_populates="role")
