from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template




@app.get("/see_all_lessons")
async def see_all_lessons():
    resp = get(f"{BASE_BACKEND_URL}/lessons")
    lessons = resp.json()
    print(lessons)
    return await render_template("see.html",resp=lessons,type="lesson")

