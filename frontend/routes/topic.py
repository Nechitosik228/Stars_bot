from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request




@app.get("/see_all_topics")
async def see_all_topics():
    resp = get(f"{BASE_BACKEND_URL}/topics")
    topics = resp.json()
    print(topics)
    return await render_template("see.html",resp=topics,type="topic",url="update_topic",delete_url="delete_one_topic")



@app.get("/see_one_topic")
async def see_one_topic():
    return await render_template("see_or_delete_form.html",url="see_one_topic_post")


@app.post("/see_one_topic")
async def see_one_topic_post():
    id = (await request.form)["id"]
    return redirect(url_for("see_one_topic_id", id=id))

@app.get("/see_one_topic/<int:id>")
async def see_one_topic_id(id):
    resp = get(f"{BASE_BACKEND_URL}/topics/{id}")
    topic = resp.json()
    return await render_template("see_one_item.html",resp=topic,type="topic",id=id)


@app.get("/update_topic")
async def update_topic():
    return await render_template("update.html",url="update_topic_post", type="topic")



@app.post("/update_topic")
async def update_topic_post():
    id = (await request.form)["id"]
    name = (await request.form)["name"]
    group_id = (await request.form)["group_id"]
    data = {"name":name,
            "group_id":group_id}
    resp = put(f"{BASE_BACKEND_URL}/topics/{id}", json=data)
    print(resp)
    return redirect(url_for("see_one_topic_id", id=id))


@app.get("/delete_one_topic")
async def delete_one_topic():
    return await render_template("see_or_delete_form.html",url="delete_one_topic_post")


@app.post("/delete_one_topic")
async def delete_one_topic_post():
    id = (await request.form)["id"]
    resp = delete(f"{BASE_BACKEND_URL}/topics/{id}")
    print(resp)
    return redirect(url_for("see_all_topics"))

@app.get("/delete_all_topics")
async def delete_all_topics():
    return await render_template("delete_all.html",url="delete_all_topics_post")


@app.post("/delete_all_topics")
async def delete_all_topics_post():
    answer = (await request.form)["answer"]
    print(answer)
    if answer == "yes":
        resp = delete(f"{BASE_BACKEND_URL}/topics")
        print(resp)
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("see_all_topics"))
    



@app.get("/create_topic")
async def create_topic():
    return await render_template("create.html", type="topic",url="create_topic_post")


@app.post("/create_topic")
async def create_topic_post():
    name = (await request.form)["name"]
    group_id = (await request.form)["group_id"]
    data = {"name":name,
            "group_id":group_id}
    resp = post(f"{BASE_BACKEND_URL}/topics", json=data)
    print(resp)
    return redirect(url_for("see_all_topics"))