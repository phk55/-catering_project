from flask import Flask, Blueprint
from apps.cms.views import bp as cms_bp
import config
from flask_caching import Cache


from exit import redis_db, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    redis_db.init_app(app)
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
