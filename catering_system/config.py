# encoding:utf-8
import os
from datetime import timedelta
import datetime

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(hours=10)
SESSION_REFRESH_EACH_REQUEST = True

DEBUG = True

USER_ID='UID'

# 缓存的ip, 端口， 数据库
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 1

REDIS_URL = "redis://localhost:6379/1"

DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'catering_score_data'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=DB_USERNAME,
                                                                                        password=DB_PASSWORD,
                                                                                        host=DB_HOST, port=DB_PORT,
                                                                                        db=DB_NAME
                                                                                        )
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 七牛云配置
# UEditor的相关配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "yvIkBLZWYNsRefcCkwDem5CoEwqcLkuyNgrvvwAk"
UEDITOR_QINIU_SECRET_KEY = "e18eaMAEMPfqc2Vu2WtEbxpZo-HP2YqZP40Q-bmz"
UEDITOR_QINIU_BUCKET_NAME = "apdatabase"
UEDITOR_QINIU_DOMAIN = "http://qlf6t33mk.hn-bkt.clouddn.com/"  # 七牛云域名

SCORE_DICT = {
    '不推荐': 1,
    '一般': 2,
    '不错': 3,
    '很棒': 4,
    '极力推荐！': 5,
}  # 评分对应的分数

SCORE_URL = 'http://127.0.0.1:5000/score/'  # 评分页面网，后接菜品id

START_TIME = datetime.date(2020, 8, 5)

# 互亿短信配置
ACCOUNT = 'C10530451'
PWD = '7e1ce8c774836315b443ebfb32052d8f'
# 注册邀请码
INVITE = '12345678'
