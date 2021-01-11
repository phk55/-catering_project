from functools import wraps
import config
from flask import session, url_for, redirect, g


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner
