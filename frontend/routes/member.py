from . import app,BASE_BACKEND_URL,SeeItem
from requests import post,get,put,delete
from quart import render_template,redirect,url_for,request





@app.get("/see_all_members")
async def see_all_members():
    resp = get(f"{BASE_BACKEND_URL}/members")
    members = resp.json()
    print(members)
    return await render_template("see.html",resp=members,type="member")


@app.get("/see_one_member")
async def see_one_member():
    print(SeeItem())
    return await render_template("see_one_item_form.html",form=SeeItem())


@app.post("/see_one_member")
async def see_one_member_():
    return await redirect(url_for("see_one_member_id"))

@app.get("/see_one_member/<int:id>")
async def see_one_member_id(id):
    resp = get(f"{BASE_BACKEND_URL}/members/{id}")
    member = resp.json()
    return await render_template("see_one_item.html",resp=member,type="member")