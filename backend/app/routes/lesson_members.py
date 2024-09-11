from sqlalchemy import select,update
from ..db import Config,LessonMember
from ..schemas import LessonMemberData,UpdateLessonMemberData
from .. import app

Session = Config.SESSION

@app.post("/lesson_members")
def create_lesson_members(data: LessonMemberData):
    with Session.begin() as session:
        lesson_member= LessonMember(**data.model_dump())
        session.add(lesson_member)
        return lesson_member
        


@app.get("/lesson_members/{lesson_id}/{member_id}")
def get_lesson_member(lesson_id:int, member_id:int):
    with Session.begin() as session:
        member = session.scalar(select(LessonMember).where(LessonMember.lesson_id==lesson_id).where(LessonMember.member_id==member_id))
        data = {
            "member_id": member.member_id,
            "stars": member.stars_count
        }
        return data
    


@app.get("/lesson_members/{lesson_id}")
def get_lesson_members(lesson_id:int):
    with Session.begin() as session:
        members = session.scalars(select(LessonMember).where(LessonMember.lesson_id==lesson_id)).all()
        return members

        
        
    
@app.put("/lesson_members/{lesson_id}/{member_id}")
def upd_lesson_member(lesson_id:int,member_id:int,data:UpdateLessonMemberData):
    with Session.begin() as session:
        member = session.scalar(select(LessonMember).where(LessonMember.lesson_id==lesson_id).where(LessonMember.member_id==member_id))
        upd = update(LessonMember).where(LessonMember.lesson_id == lesson_id).where(LessonMember.member_id == member_id).values(
            stars_count=data.stars_count
        )
        session.execute(upd)
        return member



@app.delete("/lesson_members/{lesson_id}")
def del_lesson_members(lesson_id:int):
    with Session.begin() as session:
        lesson_members = session.scalars(select(LessonMember).where(LessonMember.lesson_id==lesson_id))
        session.delete(lesson_members)


@app.delete("/lesson_members/{lesson_id}/{member_id}")
def del_lesson_member(lesson_id:int,member_id:int):
    with Session.begin() as session:
        member = session.scalar(select(LessonMember).where(LessonMember.lesson_id==lesson_id).where(LessonMember.member_id==member_id))
        session.delete(member)

       