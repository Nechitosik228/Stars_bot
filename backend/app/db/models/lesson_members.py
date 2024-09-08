from .config import Config
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey


class LessonMembersAssoc(Config.BASE):
    """Assoc table for lessons and members"""

    lesson: Mapped["Lesson"] = relationship()
    lesson_id: int = mapped_column(ForeignKey("lessons.id"))

    member: Mapped["Member"] = relationship()
    member_id: int = mapped_column(ForeignKey("members.id"))

    stars_count: int  # TODO: check if stars_count <= 5 and >= 0
