# encoding:utf-8
from exit import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_menu = db.Table(
    'user_menu',
    db.Column('user_id', db.Integer, db.ForeignKey('cms_user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), primary_key=True)
)


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(2000), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    TAG = db.Column(db.String(20), nullable=False, default=1)  # 代表这个员工还在不在,0代表离职。1代表在职厨师.2代表管理员
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, phone_number, TAG):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.TAG = TAG

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
    menu_num = db.Column(db.String(3), nullable=False)
    pic_name = db.Column(db.Text)
    ewm_name = db.Column(db.Text)
    sold_out = db.Column(db.Integer, default=0)  # 1.为已下架
    describe_info = db.Column(db.Text)

    menu_to_users = db.relationship('CMSUser', secondary=user_menu, backref=('menus', {'lazy': 'dynamic'}))


class ScoreModel(db.Model):
    __tablename__ = 'score_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    server = db.Column(db.Integer, nullable=False)
    chefs = db.Column(db.Text)
    suggest = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

    score_menu = db.relationship('MenuModels', backref=db.backref('menu_score', lazy='dynamic'))

    def get_data(self):
        score_data = {
            'score': self.score,
            'server': self.server,
            'suggest': self.suggest,
            'create_time': str(self.create_time)
        }
        return score_data


# class DiningTableModel(db.Model):
#     __tablename__ = 'dining_table'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     table_num = db.Column(db.Integer, nullable=False)
#
#
# class ServerScoreModel(db.Model):
#     __tablename__ = 'server_score'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     server = db.Column(db.Integer, nullable=False)
#     suggest = db.Column(db.Text)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#
#     table_num_id = db.Column(db.Integer, db.ForeignKey('dining_table.id'), nullable=False)
#
#     dining_tables = db.relationship('DiningTableModel', backref=db.backref('servers', lazy='dynamic'))
#
#     def get_data(self):
#         server_data = {
#             'server': self.server,
#             'suggest': self.suggest,
#             'create_time': str(self.create_time)
#         }
#         return server_data
