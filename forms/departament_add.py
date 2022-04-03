from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    chief = StringField('chief', validators=[DataRequired()])
    title = StringField('title')
    members = StringField("members")
    email = StringField('email')
    submit = SubmitField('Применить')