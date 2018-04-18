#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
# session_protection属性可以设置为None， basic， strong，以提供
# 不同的安全等级防止用户会话遭篡改
login_manager = LoginManager()
# 为strong时，会记录客户端ip地址和浏览器用户代理信息
login_manager.session_protection = 'strong'
# 设置登陆页面的端点
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 注册认证蓝本url_prefix是可选参数，为所有注册后的蓝本加上指定前缀
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # 初始化
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app
