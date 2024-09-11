from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template




@app.get("/see_all_topics")
async def see_all_topics():
    resp = get(f"{BASE_BACKEND_URL}/topics")
    topics = resp.json()
    print(topics)
    return await render_template("see.html",resp=topics,type="topic")