#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# 获取config当前所在的目录路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    定义基类
    """
    # 从系统环境变量获取SECRET_KEY 保证key不泄露,没有使用字符串'hard to guess string'
    # 用于验证表单提交数据的真伪，防止CSRF发生
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 设为True之后每次请求都会自动提交数据库的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 邮件服务器配置信息
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[项目版本统计系统]'
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# 定义字典注册不同的配置环境，而且还注册了一个默认的配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
