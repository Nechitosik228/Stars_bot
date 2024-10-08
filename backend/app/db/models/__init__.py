from .config import Config
from .role import Role
from .member import Member
from .topic import Topic
from .lesson import Lesson
from .group import Group
from .lesson_members import LessonMember

DB_MODELS = {
    "Roles": Role,
    "Members": Member,
    "Topics": Topic,
    "Lessons": Lesson,
    "Groups": Group,
    "LessonMembers": LessonMember
}
