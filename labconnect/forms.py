from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeField,
    IntegerField,
    PasswordField,
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

"""
Forms
"""


class PostOpportunity(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField("Submit")
