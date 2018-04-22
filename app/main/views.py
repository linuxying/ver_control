#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from . import main
from ..models import Project, Permission
from flask_login import login_required
from ..decorators import admin_required, permission_required


@main.route('/')
@login_required
def index():
    projects = Project.query.all()
    projects_list = Project.query.first()
    return render_template('index.html', projects=projects, projects_list=projects_list)
    # return render_template(url_for('main.index'), projects=projects, projects_list=projects_list)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"
