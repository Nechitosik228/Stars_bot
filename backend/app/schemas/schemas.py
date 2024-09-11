from pydantic import BaseModel


class LessonMemberData(BaseModel):
    member_id:int
    lesson_id:int
    stars_count:int


class UpdateLessonMemberData(BaseModel):
    stars_count:int