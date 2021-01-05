from flask import g,session
from ..cms.views import bp as cms_bp
from ..front.views import bp as front_bp
import config
from ..cms.models import CMSUser


@cms_bp.before_request
@front_bp.before_request
def before_request():
    g.qiniu_url = config.UEDITOR_QINIU_DOMAIN

@cms_bp.before_request
def before_request():
    if config.USER_ID in session:
        user_id = session.get(config.USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user