from quart import ResponseReturnValue, redirect, url_for
from quart_auth import Unauthorized
from . import app
from .auth import sign_in


@app.errorhandler(Unauthorized)
async def redirect_to_login(*_: Exception) -> ResponseReturnValue:
    return redirect(url_for(sign_in.__name__))
