from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand  # 导入
from flask_script import Manager  # 导入

from apps.models.model import *

Migrate(app ,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
    # python manage.py db init
    # python manage.py db migrate
    # python manage.py db upgrade
    # netstat -tlnp|grep 8081d