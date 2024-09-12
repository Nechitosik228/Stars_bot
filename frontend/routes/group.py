from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request




@app.get("/see_all_groups")
async def see_all_groups():
    resp = get(f"{BASE_BACKEND_URL}/groups")
    groups = resp.json()
    print(groups)
    return await render_template("see.html",resp=groups,type="group",url="update_group",delete_url="delete_one_group")



@app.get("/see_one_group")
async def see_one_group():
    return await render_template("see_or_delete_form.html",url="see_one_group_post")


@app.post("/see_one_group")
async def see_one_group_post():
    id = (await request.form)["id"]
    return redirect(url_for("see_one_group_id", id=id))

@app.get("/see_one_group/<int:id>")
async def see_one_group_id(id):
    resp = get(f"{BASE_BACKEND_URL}/groups/{id}")
    group = resp.json()
    return await render_template("see_one_item.html",resp=group,type="group",id=id)


@app.get("/update_group")
async def update_group():
    return await render_template("update.html",url="update_group_post", type="group")



@app.post("/update_group")
async def update_group_post():
    id = (await request.form)["id"]
    name = (await request.form)["name"]
    data = {"name":name}
    resp = put(f"{BASE_BACKEND_URL}/groups/{id}", json=data)
    print(resp)
    return redirect(url_for("see_one_group_id", id=id))


@app.get("/delete_one_group")
async def delete_one_group():
    return await render_template("see_or_delete_form.html",url="delete_one_group_post")


@app.post("/delete_one_group")
async def delete_one_group_post():
    id = (await request.form)["id"]
    resp = delete(f"{BASE_BACKEND_URL}/groups/{id}")
    print(resp)
    return redirect(url_for("see_all_groups"))

@app.get("/delete_all_groups")
async def delete_all_groups():
    return await render_template("delete_all.html",url="delete_all_groups_post")


@app.post("/delete_all_groups")
async def delete_all_groups_post():
    answer = (await request.form)["answer"]
    print(answer)
    if answer == "yes":
        resp = delete(f"{BASE_BACKEND_URL}/groups")
        print(resp)
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("see_all_groups"))
    



@app.get("/create_group")
async def create_group():
    return await render_template("create.html", type="group",url="create_group_post")


@app.post("/create_group")
async def create_group_post():
    name = (await request.form)["name"]
    data = {"name":name}
    resp = post(f"{BASE_BACKEND_URL}/groups", json=data)
    print(resp)
    return redirect(url_for("see_all_groups"))