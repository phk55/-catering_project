# encoding:utf-8

from ..common_func.forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class LoginForm(BaseForm):
    phone = StringField(validators=[InputRequired(message='请输入手机号码！')])
    pwd = StringField(validators=[InputRequired(message='请输入密码！')])
    verify = StringField(validators=[InputRequired(message='请输入验证码！')])


class SignupForm(BaseForm):
    username = StringField(validators=[Regexp(r'.{2,3}', message='请输入正确格式的用户名！')])
    phone = StringField(validators=[InputRequired(message='请输入手机号码！')])
    pwd = StringField(validators=[InputRequired(message='请输入密码！')])
    verify = StringField(validators=[InputRequired(message='请输入验证码！')])
    invite = StringField(validators=[InputRequired(message='请输入邀请码！')])
