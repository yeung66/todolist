from flask import url_for, render_template, redirect, session, flash, request
from ..model import User, Task
from .forms import UserForm
from . import main
from .. import db


@main.route('/')
def index():
    if 'user' in session:
        user = User.query.get(session['user'])
        tasks = user.tasks
        return render_template('index.html', username=user.username, tasks=tasks)
    return render_template('index.html', form=UserForm())


@main.route('/user', methods=['POST'])
def user_admin():
    form = UserForm()
    if form.validate_on_submit():
        login = form.login.data
        user = User.query.filter_by(username=form.username.data).first()
        msg = None
        if login:
            if user is None:
                msg = '用户不存在！'
            elif user.password != form.password.data:
                msg = '用户名或密码错误！'
            else:
                session['user'] = user.username
        else:
            if user is None:
                msg = '注册成功！'
                user = User(username=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                session['user'] = user.username
            else:
                msg = '用户名已存在'
        if msg is not None: flash(msg)
    return redirect(url_for('.index'))


@main.route('/logout')
def logout():
    session.pop('user', None)
    # session.pop('password', None)
    return redirect(url_for('.index'))


@main.route('/addTask', methods=['POST'])
def add_task():
    msg = None

    if 'user' not in session:
        msg = '请先登录再添加任务！'
    elif not User.query.get(session['user']):
        msg = '用户不存在！请重新登录'
        session.pop('user')
    else:
        task_name = request.form['content']
        task = Task(content=task_name, username=session['user'])
        db.session.add(task)
        db.session.commit()
        msg = '添加任务成功！'
    return redirect(url_for('.index'))


@main.route('/done/<id>')
def done(id):
    # id = request.form['id']
    task = Task.query.get(id)
    # msg = None
    if task and 'user' in session and session['user'] == task.username:
        task.finished = True
        db.session.commit()
    return redirect(url_for('.index'))


@main.route('/del/<id>')
def delete(id):
    task = Task.query.get(id)
    if task and 'user' in session and session['user'] == task.username:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('.index'))

