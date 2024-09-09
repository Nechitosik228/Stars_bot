from quart import redirect, render_template, request
from . import app


@app.get("/")
async def index():
    return await render_template("index.html", title=__name__)
