from flask import render_template
from . import app
from bot import request_provider, Method, BASE_BACKEND_URL


@app.get("/see_all_members")
def see_all_members():
    url = BASE_BACKEND_URL + "/members"
    resp = request_provider(url, method=Method.GET)
    print(resp)
    return render_template("members.html", members=resp)

@app.post("/create_member")
def create_member():
    ...


@app.delete("/delete_all_members")
def delete_all_member():
    url = BASE_BACKEND_URL + "/members"
    resp = request_provider(url, method=Method.DELETE)
    print(resp)
    return render_template("members.html")