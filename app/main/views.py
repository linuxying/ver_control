#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, abort, redirect, url_for, flash, request
from . import main
from ..models import Project, User, db, Host
from flask_login import login_required, current_user
from ..decorators import admin_required
from .froms import ProjectForm, HostForm


@main.route('/')
@login_required
def index():
    usersnum = len(User.query.all())
    hostsnum = len(Host.query.all())
    old_projects = Project.query.all()
    # 定义一个空列表，目的是为了去除重复的项目名称
    projects = []
    for p in old_projects:
        if p.projectname not in projects:
            projects.append(p.projectname)
    projectsnum = len(projects)
    return render_template('index.html', projectsnum=projectsnum, usersnum=usersnum, hostsnum=hostsnum)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/hosts')
@login_required
def hosts():
    """
    主机列表管理
    :return: 返回主机列表到hosts.html
    """
    hosts = Host.query.all()
    return render_template('hosts.html', hosts=hosts)


@main.route('/add-host', methods=['GET', 'POST'])
@login_required
def add_host():
    form = HostForm()
    if form.validate_on_submit():
        host = Host(hostname=form.hostname.data, ip=form.ip.data, port=form.port.data,
                    cpu=form.cpu.data, memory=form.memory.data, disk=form.disk.data,
                    system=form.system.data, create_user=current_user.username, create_date=form.create_date.data)
        db.session.add(host)
        db.session.commit()
        flash('添加主机成功!')
        return redirect(url_for('main.hosts'))
    return render_template('add_host.html', form=form)


@main.route('/del-host/<id>')
@login_required
def del_host(id):
    host = Host.query.filter_by(id=id).first()
    db.session.delete(host)
    db.session.commit()
    hosts = Host.query.all()
    flash('已删除主机！')
    return render_template('hosts.html', hosts=hosts)


@main.route('/edit-host/<id>', methods=['GET', 'POST'])
@login_required
def edit_host(id):
    form = HostForm()
    host = Host.query.get_or_404(id)
    if form.validate_on_submit():
        host.hostname = form.hostname.data
        host.ip = form.ip.data
        host.port = form.port.data
        host.cpu = form.cpu.data
        host.memory = form.memory.data
        host.disk = form.disk.data
        host.system = form.system.data
        host.create_date = form.create_date.data
        hosts = Host.query.all()
        flash('数据更新成功！')
        return render_template('hosts.html', hosts=hosts)
    form.hostname.data = host.hostname
    form.ip.data = host.ip
    form.port.data = host.port
    form.cpu.data = host.cpu
    form.system.data = host.system
    form.memory.data = host.memory
    form.disk.data = host.disk
    form.create_date.data = host.create_date
    return render_template('edit_host.html', form=form)


@main.route('/host-detail/<id>')
@login_required
def host_detail(id):
    host = Host.query.filter_by(id=id).first()
    return render_template('host_detail.html', host=host)


@main.route('/projects')
@login_required
def projects():
    """
    项目列表管理
    :return: 返回项目列表到projects.html
    """
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


@main.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(projectname=form.projectname.data, date=form.date.data, env=form.env.data,
                          dev_ver=form.dev_ver.data, rel_ver=form.rel_ver.data, path=form.path.data,
                          remark=form.remark.data, user=current_user, log_dir=form.log_dir.data,
                          host=form.host.data)
        db.session.add(project)
        db.session.commit()
        flash('添加项目成功！')
        return redirect(url_for('main.projects'))
    return render_template('add_project.html', form=form)


@main.route('/del-project/<id>')
@login_required
def del_project(id):
    project = Project.query.filter_by(id=id).first()
    db.session.delete(project)
    db.session.commit()
    flash('删除项目成功！')
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


@main.route('/edit-project/<id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.projectname = form.projectname.data
        project.date = form.date.data
        project.env = form.env.data
        project.dev_ver = form.dev_ver.data
        project.rel_ver = form.rel_ver.data
        project.path = form.path.data
        project.remark = form.remark.data
        project.log_dir = form.log_dir.data
        project.host = form.host.data
        db.session.add(current_user)
        flash('数据更新成功')
        return redirect(url_for('main.projects'))
    form.projectname.data = project.projectname
    form.date.data = project.date
    form.env.data = project.env
    form.dev_ver.data = project.dev_ver
    form.rel_ver.data = project.rel_ver
    form.path.data = project.path
    form.remark.data = project.remark
    form.host.data = project.host
    form.log_dir.data = project.log_dir
    return render_template('edit_project.html', form=form)


@main.route('/project-detail/<id>')
@login_required
def project_detail(id):
    """
    定义项目详单函数，传入参数为项目名称
    """
    projects = Project.query.filter_by(id=id).first()
    userid = projects.user.id
    user = User.query.filter_by(id=userid).first()
    return render_template('project_detail.html', projects=projects, user=user)


@main.route('/users')
@login_required
def users():
    """
    用户列表
    :return:返回用户信息
    """
    users = User.query.all()
    return render_template('users.html', users=users)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"
