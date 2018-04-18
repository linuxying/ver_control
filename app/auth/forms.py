#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('login in')


class RegistrationFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Username must be letters,'
                                                                                         'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        # 验证邮箱是否存在
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registred.')

    def validate_username(self, field):
        #  验证用户名是否存在
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist.')
