from flask import render_template
from . import app
from bot import request_provider, Method, BASE_BACKEND_URL


@app.get("/see_all_lessons")
def see_all_lessons():
    url = BASE_BACKEND_URL + "/lessons"
    resp = request_provider(url, method=Method.GET)
    print(resp)
    return render_template("lessons.html", members=resp)