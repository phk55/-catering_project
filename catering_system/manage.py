# encoding:utf-8

from catering_score import create_app, db
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from apps.cms import models as cms_models

app = create_app()
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()
