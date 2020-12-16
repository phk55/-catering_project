# encoding:utf-8
from flask import Blueprint,render_template
from exit import redis_db

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
def index():
    redis_p = redis_db.pipeline()
    redis_p.set('ss3','fsdfd2')
    redis_p.execute()
    return render_template('cms/cms_index.html')


@bp.route('/menulist/')
def menulist():
    return render_template('cms/menulist.html')