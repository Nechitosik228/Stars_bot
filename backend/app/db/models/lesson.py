from datetime import datetime
from typing import List
from .config import Config
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Lesson(Config.BASE):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column()

    topic: Mapped["Topic"] = relationship(back_populates="lessons")
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))

    lesson_members: Mapped[List["LessonMember"]] = relationship(back_populates="lesson")



datetime.strptime