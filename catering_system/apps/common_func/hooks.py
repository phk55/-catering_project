from flask import g
from ..cms.views import bp as cms_bp
from ..front.views import bp as front_bp
import config


@cms_bp.before_request
@front_bp.before_request
def before_request():
    g.qiniu_url = config.UEDITOR_QINIU_DOMAIN

