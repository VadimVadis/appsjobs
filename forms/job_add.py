from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = StringField('team_leader', validators=[DataRequired()])
    job = StringField('job')
    work_size = IntegerField("work_size")
    collaborators = StringField("collaborators")
    start_date = DateField("start_date")
    end_date = DateField("end_date")
    is_finished = BooleanField("is_finished")
    submit = SubmitField('Применить')