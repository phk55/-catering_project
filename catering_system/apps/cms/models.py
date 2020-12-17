# encoding:utf-8
from exit import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(2000), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, phone_number):
        self.username = username
        self._password = password
        self.phone_number = phone_number

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)
        return

    def check_password(self, raw_password):
        result = check_password_hash(self._password, raw_password)
        return result


class MenuModels(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_name = db.Column(db.String(20), nullable=False)
    weighted_value = db.Column(db.Integer, nullable=False)
    pic_name = db.Column(db.Text)
    describe_info = db.Column(db.Text)