from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    brand = SelectField('Бренд', coerce=int, validators=[DataRequired()])
    model = StringField('Модель', validators=[DataRequired()])
    text = TextAreaField("Текст")
    submit = SubmitField('Сохранить')

