#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
# 使用werkzeug实现密码散列
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(UserMixin, db.Model):
    """
    定义用户表，表名users，id和username两个字段，id为主键，username唯一且建立索引
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', backref='user')
    confirmed = db.Column(db.Boolean, default=False)

    # property装饰器作用是把password函数变成类的属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # passowrd又创建了另一个装饰器password.setter，也是类的属性
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码结果是否为True
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        # 生成token，过期时间为3600秒后self.id为用户id
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        # 验证token，如果验证通过，则把新添加的confirmed属性设置为True
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
