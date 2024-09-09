from quart_auth import (
    AuthUser,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from quart import redirect, render_template, request
from quart_wtf import QuartForm


from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import PasswordInput, SubmitInput

from . import app


class CreateAccountForm(QuartForm):
    email = EmailField(
        "Email address",
        validators=[DataRequired("Please enter your email address"), Email()],
    )

    password = PasswordField(
        "Password",
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired("Please enter your password"),
            EqualTo("password_confirm", message="Passwords must match"),
        ],
    )

    password_confirm = PasswordField(
        "Confirm Password",
        widget=PasswordInput(hide_value=False),
        validators=[DataRequired("Please confirm your password")],
    )

    name = StringField("Ім'я", validators=[DataRequired("Please enter your name")])
    register = SubmitField("Зареєструватись")


@app.get("/login")
async def sign_in():
    return await render_template("login.html", form=CreateAccountForm())


@app.post("/login")
async def sign_in_post():
    # Check Credentials here, e.g. username & password.
    ...
    # We'll assume the user has an identifying ID equal to 2
    login_user(AuthUser(2))
    ...


@app.route("/logout")
async def logout():
    logout_user()
    ...
