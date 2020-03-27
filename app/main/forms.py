from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField('用户名', [DataRequired()])
    password = PasswordField('密码', [DataRequired()])
    login = SubmitField('登录', id='login')
    signup = SubmitField('注册', id='signup')