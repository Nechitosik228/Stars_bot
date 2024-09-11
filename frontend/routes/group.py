from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from quart import render_template




@app.get("/see_all_groups")
async def see_all_groups():
    resp = get(f"{BASE_BACKEND_URL}/groups")
    groups = resp.json()
    print(groups)
    return await render_template("see.html",resp=groups,type="group")