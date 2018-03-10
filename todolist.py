from flask import Flask,request,render_template,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:*******@localhost/todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key=os.urandom(24)
app.debug=True
db = SQLAlchemy(app,use_native_unicode='utf-8')

test_user = '中文'

class Task(db.Model):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(30))
    content = db.Column(db.String(50))
    finished = db.Column(db.BOOLEAN)

    def __repr__(self):
        return '<Task %s>' % self.content

class User(db.Model):
    username = db.Column(db.String(30),primary_key=True)
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<User %s>' % self.username



@app.route('/')
def hello_world():
    if session.get('username') and session.get('password'):
        user = User.query.get(session.get('username'))
        if user:
            tasks = Task.query.filter_by(username=user.username).all()
            return render_template('extend.html',tasks=tasks,user=user.username)
    return render_template('non_login.html')

@app.route('/signup',methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if not User.query.get('username'):
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['password'] = password
        return redirect(url_for('hello_world'))
    return "用户已存在"

@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.get(username)
    if user:
        if user.password != password: return '密码错误！'
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('hello_world'))
    return "用户不存在！"

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('password',None)
    return redirect(url_for('hello_world'))

@app.route('/addTask',methods=['POST'])
def add_task():
    n = session.get('username')
    if n is None:return "请先登录！"
    c = request.form['content']
    new_task = Task(username=n,content=c,finished=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('hello_world'))

@app.route('/done/<id>')
def done(id):
    #id = request.form['id']
    task = Task.query.get(id)
    if task:
        task.finished=True
        db.session.commit()
        return redirect(url_for('hello_world'))
    return "error"

@app.route('/del/<id>')
def delete(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('hello_world'))
    return "error"

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
