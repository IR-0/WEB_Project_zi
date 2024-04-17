from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    content = StringField("Укажите свой номер", validators=[DataRequired()])
    submit = SubmitField('Применить')
