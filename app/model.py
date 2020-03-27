from app import db


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(20))
    tasks = db.relationship('Task', backref='user')

    def __repr__(self):
        return '<User %s>' % self.username


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('users.username'))
    content = db.Column(db.String(50))
    finished = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return '<Task %s>' % self.content