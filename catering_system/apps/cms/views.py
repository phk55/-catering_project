# encoding:utf-8
from flask import Blueprint
from exit import redis_db

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
def index():
    redis_p = redis_db.pipeline()
    redis_p.set('ss3','fsdfd2')
    redis_p.execute()
    return 'hello world'
