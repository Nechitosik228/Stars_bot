from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request





@app.get("/see_all_lessons")
async def see_all_lessons():
    resp = get(f"{BASE_BACKEND_URL}/lessons")
    lessons = resp.json()
    print(lessons)
    return await render_template("see.html",resp=lessons,type="lesson",url="update_lesson",delete_url="delete_one_lesson")

@app.get("/see_one_lesson")
async def see_one_lesson():
    return await render_template("see_or_delete_form.html",url="see_one_lesson_post")


@app.post("/see_one_lesson")
async def see_one_lesson_post():
    id = (await request.form)["id"]
    return redirect(url_for("see_one_lesson_id", id=id))

@app.get("/see_one_lesson/<int:id>")
async def see_one_lesson_id(id):
    resp = get(f"{BASE_BACKEND_URL}/lessons/{id}")
    lesson = resp.json()
    return await render_template("see_one_item.html",resp=lesson,type="lesson",id=id)


@app.get("/update_lesson")
async def update_lesson():
    return await render_template("update.html",url="update_lesson_post", type="lesson")



@app.post("/update_lesson")
async def update_lesson_post():
    id = (await request.form)["id"]
    date = (await request.form)["date"]
    topic_id = (await request.form)["topic_id"]
    data = {"date":date,
            "topic_id":topic_id,}
    resp = put(f"{BASE_BACKEND_URL}/lessons/{id}", json=data)
    print(resp)
    return redirect(url_for("see_one_lesson_id", id=id))


@app.get("/delete_one_lesson")
async def delete_one_lesson():
    return await render_template("see_or_delete_form.html",url="delete_one_lesson_post")


@app.post("/delete_one_lesson")
async def delete_one_lesson_post():
    id = (await request.form)["id"]
    resp = delete(f"{BASE_BACKEND_URL}/lessons/{id}")
    print(resp)
    return redirect(url_for("see_all_lessons"))

@app.get("/delete_all_lessons")
async def delete_all_lessons():
    return await render_template("delete_all.html",url="delete_all_lessons_post")


@app.post("/delete_all_lessons")
async def delete_all_lessons_post():
    answer = (await request.form)["answer"]
    print(answer)
    if answer == "yes":
        resp = delete(f"{BASE_BACKEND_URL}/lessons")
        print(resp)
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("see_all_lessons"))
    



@app.get("/create_lesson")
async def create_lesson():
    return await render_template("create.html", type="lesson",url="create_lesson_post")


@app.post("/create_lesson")
async def create_lesson_post():
    date = (await request.form)["date"]
    topic_id = (await request.form)["topic_id"]
    data = {"date":date,
            "topic_id":topic_id}
    resp = post(f"{BASE_BACKEND_URL}/lessons", json=data)
    print(resp)
    return redirect(url_for("see_all_lessons"))