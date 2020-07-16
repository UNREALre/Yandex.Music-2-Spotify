# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Optional


class BaseForm(FlaskForm):
    class Meta:
        locales = ['ru']


class AuthForm(BaseForm):
    login = StringField('Логин', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    captcha_answer = StringField('Введите символы с картинки', validators=[DataRequired()])
    captcha_key = HiddenField()
    submit = SubmitField('Далее')
