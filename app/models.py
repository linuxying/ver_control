#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
from datetime import datetime


class User(db.Model):
    """
    定义用户表，表名users，id和username两个字段，id为主键，username唯一且建立索引
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    projects = db.relationship('Project', backref='user')

    def __repr__(self):
        return '<User %s>' % self.username


class Project(db.Model):
    """
    定义项目表，表明projects
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(256), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    env = db.Column(db.String(64), nullable=False)
    dev_ver = db.Column(db.String(256), nullable=False)
    rel_ver = db.Column(db.String(256), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    remark = db.Column(db.Text)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Project %s>' % self.projectname
