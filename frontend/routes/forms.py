from quart_wtf import QuartForm
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    SubmitField,
)
from wtforms.validators import DataRequired



class SeeItem(QuartForm):
    id = StringField("Id", validators=[DataRequired("Please enter id")])
    submit = SubmitField("Submit")





