from .config import Config
from sqlalchemy.orm import Mapped

class LessonMembersAssoc(Config.BASE):
    """Assoc table for lessons and members"""

    lesson: Mapped["Lesson"]
    lesson_id: int

    member: Mapped["Member"]
    member_id: int

    stars_count: int  # TODO: check if stars_count <= 5 and >= 0
    ...
