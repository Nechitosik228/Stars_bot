from flask import render_template
from . import app
from bot import request_provider, Method, BASE_BACKEND_URL


@app.get("/see_all_groups")
def see_all_groups():
    url = BASE_BACKEND_URL + "/groups"
    resp = request_provider(url, method=Method.GET)
    print(resp)
    return render_template("groups.html", members=resp)