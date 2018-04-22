#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
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
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # property装饰器作用是把password函数变成类的属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # passowrd又创建了另一个装饰器password.setter，也是类的属性
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # 验证密码结果是否为True
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        # 生成验证token，过期时间为3600秒后self.id为用户id
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        # 生成重设密码连接token，过期时间为3600秒，self.id为用户id
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

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

    def reset_password(self, token, new_password):
        # 验证token，如果验证通过，则吧新添加的password更新
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(self, Permission.ADMINISTER)

    def __repr__(self):
        return '<User %s>' % self.username


class AnonymousUser(AnonymousUserMixin):
    """
    这个对象继承自Flask-Login中的AnonymousUserMixin 类，并将其设为用户未登录时
    current_user 的值。这样程序不用先检查用户是否登录，就能自由调用current_user.can() 和
    current_user.is_administrator()。
    """
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    """
    定义用户角色，管理员、普通用户等
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    # permissions值是一个整数，表示位标志。各操作都对应一个位位置，能执行某项操作的角色，其位会被设为1。
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT |
                          Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    """
    定义权限，普通用户和管理员用户
    """
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


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
    # Flask-Login要求实现一个回调函数,使用 get_id()方法返回的唯一标识用户的Unicode字符串 作为参数 返回这个用户对象.
    # 如果是继承的UserMixin类, get_id()方法默认返回的用户的id. 如果用户不存在,应该返回None.
    return User.query.get(int(user_id))
