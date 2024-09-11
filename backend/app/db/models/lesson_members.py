from .config import Config
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey


class LessonMember(Config.BASE):
    __tablename__ = "lesson_members"


    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), primary_key=True)

    lesson: Mapped["Lesson"] = relationship(back_populates="lesson_members")
    member: Mapped["Member"] = relationship(back_populates="lesson_members")

    stars_count: Mapped[int]  # TODO: check if stars_count <= 5 and >= 0
