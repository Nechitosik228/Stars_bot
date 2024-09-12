from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request






@app.get("/see_all_members")
async def see_all_members():
    resp = get(f"{BASE_BACKEND_URL}/members")
    members = resp.json()
    print(members)
    return await render_template("see.html",resp=members,type="member",url="update_member",delete_url="delete_one_member")


@app.get("/see_one_member")
async def see_one_member():
    return await render_template("see_or_delete_form.html",url="see_one_member_post")


@app.post("/see_one_member")
async def see_one_member_post():
    id = (await request.form)["id"]
    return redirect(url_for("see_one_member_id", id=id))

@app.get("/see_one_member/<int:id>")
async def see_one_member_id(id):
    resp = get(f"{BASE_BACKEND_URL}/members/{id}")
    member = resp.json()
    return await render_template("see_one_item.html",resp=member,type="member",id=id)


@app.get("/update_member")
async def update_member():
    return await render_template("update.html",url="update_member_post", type="member")



@app.post("/update_member")
async def update_member_post():
    id = (await request.form)["id"]
    name = (await request.form)["name"]
    telegram_id = (await request.form)["telegram_id"]
    group_id = (await request.form)["group_id"]
    data = {"name":name,
            "telegram_id":telegram_id,
            "group_id":group_id,}
    resp = put(f"{BASE_BACKEND_URL}/members/{id}", json=data)
    print(resp)
    return redirect(url_for("see_one_member_id", id=id))


@app.get("/delete_one_member")
async def delete_one_member():
    return await render_template("see_or_delete_form.html",url="delete_one_member_post")


@app.post("/delete_one_member")
async def delete_one_member_post():
    id = (await request.form)["id"]
    resp = delete(f"{BASE_BACKEND_URL}/members/{id}")
    print(resp)
    return redirect(url_for("see_all_members"))

@app.get("/delete_all_members")
async def delete_all_members():
    return await render_template("delete_all.html",url="delete_all_members_post")


@app.post("/delete_all_members")
async def delete_all_members_post():
    answer = (await request.form)["answer"]
    print(answer)
    if answer == "yes":
        resp = delete(f"{BASE_BACKEND_URL}/members")
        print(resp)
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("see_all_members"))
    



@app.get("/create_member")
async def create_member():
    return await render_template("create.html", type="member",url="create_member_post")


@app.post("/create_member")
async def create_member_post():
    name = (await request.form)["name"]
    telegram_id = (await request.form)["telegram_id"]
    group_id = (await request.form)["group_id"]
    data = {"name":name,
            "telegram_id":telegram_id,
            "group_id":group_id,}
    resp = post(f"{BASE_BACKEND_URL}/members", json=data)
    print(resp)
    return redirect(url_for("see_all_members"))