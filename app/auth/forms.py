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
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')])
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


class ChangePasswordForm(FlaskForm):
    """
    修改密码表单
    """
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired(), EqualTo('newpassword2',
                                                                                    message='Passwords must match.')])
    newpassword2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetRequestForm(FlaskForm):
    """
    重设密码请求表单
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    """
    点击确认邮件连接后，重设密码表单
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirmed password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
