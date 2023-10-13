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
    SelectField,
    DateField,
    SelectMultipleField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea
from datetime import datetime

"""
Forms
"""


class PostOpportunity(FlaskForm):
    MAJORS = []
    COURSES = []
    name = StringField('Job Title', validators=[DataRequired(), Length(max=150, message='Job Title must be 150 characters or less')])
    description = TextAreaField('Job Description', widget=TextArea(), validators=[DataRequired(), Length(max=1500, message='Job Description must be 1500 characters or less')])
    compensation = SelectField('Mode of Compensation', choices=['Pay','Credit','Both'], validators=[DataRequired()])
    application_due = DateField('Application Due Date', format='%m/%d/%Y', validators=[DataRequired()])
    recommended_class_years = SelectMultipleField('Recommended Class Years', choices=['Freshman','Sophomore','Junior','Senior','Grad Student'])
    recommended_experiences = TextAreaField('Recommended Experiences', widget=TextArea(), validators=[Length(max=1500, message='Recommended experiences must be 1500 characters or less')])
    recommended_majors = SelectMultipleField('Recommended Majors', choices=MAJORS)
    recommended_courses = SelectMultipleField('Recommended Courses', choices=COURSES)
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    #active_semesters
    submit = SubmitField("Submit")
