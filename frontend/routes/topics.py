from flask import render_template
from . import app
from bot import request_provider, Method, BASE_BACKEND_URL


@app.get("/see_all_topics")
def see_all_topics():
    url = BASE_BACKEND_URL + "/topics"
    resp = request_provider(url, method=Method.GET)
    print(resp)
    return render_template("topics.html", members=resp)