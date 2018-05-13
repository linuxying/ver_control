#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, ValidationError, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Regexp


class ProjectForm(FlaskForm):
    """
    添加项目表单
    """
    projectname = StringField('项目名称', validators=[DataRequired(), Length(1, 64)])
    date = DateTimeField('开始时间', validators=[DataRequired()])
    env = StringField('环境', validators=[DataRequired(), Length(1, 64)])
    dev_ver = StringField('研发版本', validators=[DataRequired(), Length(1, 64)])
    rel_ver = StringField('交付版本', validators=[DataRequired(), Length(1, 64)])
    path = StringField('本地存储文件路径', validators=[DataRequired(), Length(1, 64)])
    log_dir = StringField('服务日志路径', validators=[DataRequired(), Length(1,64)])
    host = StringField('部署主机ip', validators=[DataRequired(), Length(1, 256)])
    remark = StringField('备注', validators=[DataRequired()])
    submit = SubmitField('提交')


class HostForm(FlaskForm):
    """
    添加主机
    """
    hostname = StringField('主机名', validators=[DataRequired(), Length(1, 128)])
    ip = StringField('IP地址', validators=[DataRequired(), Length(1, 32)])
    port = StringField('端口', validators=[DataRequired(), Length(1, 32)])
    cpu = StringField('CPU核数', validators=[DataRequired(), Length(1, 32)])
    memory = StringField('内存大小', validators=[DataRequired(), Length(1, 32)])
    disk = StringField('硬盘大小', validators=[DataRequired(), Length(1, 32)])
    system = StringField('操作系统', validators=[DataRequired(), Length(1, 64)])
    create_date = DateTimeField('创建时间', validators=[DataRequired()])
    submit = SubmitField('提交')
