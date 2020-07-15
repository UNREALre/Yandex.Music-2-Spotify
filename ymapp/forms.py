from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional


class BaseForm(FlaskForm):
    class Meta:
        locales = ['ru']


class AuthForm(BaseForm):
    login = StringField('Логин', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Далее')
