from . import app,BASE_BACKEND_URL
from requests import post,get,put,delete
from flask import render_template




@app.get("/see_all_members")
def see_all_members():
    resp = get(f"{BASE_BACKEND_URL}/members")
    print(resp)
    return render_template("see.html",resp=resp)