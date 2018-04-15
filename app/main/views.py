#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for
from datetime import datetime

from . import main
from .. import db
from ..models import User, Project


@main.route('/')
def index():
    projects = Project.query.all()
    projects_list = Project.query.first()
    return render_template('index.html', projects=projects, projects_list=projects_list)
    # return render_template(url_for('main.index'), projects=projects, projects_list=projects_list)
