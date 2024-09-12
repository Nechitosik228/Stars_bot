from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request

@app.get("/see_one_starcount")
async def see_one_starcount():
    return await render_template("see_or_delete_form.html",url="see_one_starcount_post",type="star_count")


@app.post("/see_one_starcount")
async def see_one_starcount_post():
    lesson_id = (await request.form)["lesson_id"]
    member_id = (await request.form)["member_id"]
    return redirect(url_for("see_one_starcount_id", lesson_id=lesson_id,member_id=member_id))

@app.get("/see_one_starcount/<int:lesson_id>/<int:member_id>")
async def see_one_starcount_id(lesson_id,member_id):
    resp = get(f"{BASE_BACKEND_URL}/lesson_members/{lesson_id}/{member_id}")
    starcount = resp.json()
    return await render_template("see_one_item.html",resp=starcount,type="starcount",lesson_id=lesson_id,member_id=member_id)


@app.get("/update_starcount")
async def update_starcount():
    return await render_template("update.html",url="update_starcount_post", type="starcount")



@app.post("/update_starcount")
async def update_starcount_post():
    lesson_id = (await request.form)["lesson_id"]
    member_id = (await request.form)["member_id"]
    star_count = (await request.form)["star_count"]
    data = {"stars_count":star_count,}
    resp = put(f"{BASE_BACKEND_URL}/lesson_members/{lesson_id}/{member_id}", json=data)
    print(resp)
    return redirect(url_for("see_one_starcount_id", lesson_id=lesson_id,member_id=member_id))


@app.get("/delete_one_starcount")
async def delete_one_starcount():
    return await render_template("see_or_delete_form.html",url="delete_one_starcount_post",type="star_count")


@app.post("/delete_one_starcount")
async def delete_one_starcount_post():
    lesson_id = (await request.form)["lesson_id"]
    member_id = (await request.form)["member_id"]
    resp = delete(f"{BASE_BACKEND_URL}/lesson_members/{lesson_id}/{member_id}")
    print(resp)
    return redirect(url_for("homepage"))


    



@app.get("/create_starcount")
async def create_starcount():
    return await render_template("create.html", type="starcount",url="create_starcount_post")


@app.post("/create_starcount")
async def create_starcount_post():
    lesson_id = (await request.form)["lesson_id"]
    member_id = (await request.form)["member_id"]
    star_count = (await request.form)["star_count"]

    data = {"lesson_id":lesson_id,
            "member_id":member_id,
            "stars_count":star_count}
    resp = post(f"{BASE_BACKEND_URL}/lesson_members", json=data)
    print(resp)
    return redirect(url_for("homepage"))