from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class get_ical(FlaskForm):
    student_id = StringField('学号：',validators=[DataRequired()])
    submit = SubmitField('获取')