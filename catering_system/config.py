# encoding:utf-8
DEBUG = True

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
