#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from . import main
from ..models import Project
from flask_login import login_required


@main.route('/')
@login_required
def index():
    projects = Project.query.all()
    projects_list = Project.query.first()
    return render_template('index.html', projects=projects, projects_list=projects_list)
    # return render_template(url_for('main.index'), projects=projects, projects_list=projects_list)
