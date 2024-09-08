from .config import Config
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey


class LessonMembersAssoc(Config.BASE):
    """Assoc table for lessons and members"""

    lesson: Mapped["Lesson"] = relationship(back_populates="members")
    lesson_id: int = mapped_column(ForeignKey("lessons.id"), primary_key=True)

    member: Mapped["Member"] = relationship(back_populates="lessons")
    member_id: int = mapped_column(ForeignKey("members.id"), primary_key=True)

    stars_count: int  # TODO: check if stars_count <= 5 and >= 0
