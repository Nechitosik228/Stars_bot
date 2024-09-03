from typing import List
from .config import Config
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Topic(Config.BASE):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    lessons: Mapped[List["Lesson"]] = relationship(back_populates="topic")
    
    group: Mapped["Group"] = relationship(back_populates="topic")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))