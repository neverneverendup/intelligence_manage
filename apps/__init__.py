from flask import Flask
from . import models, routes
from .config import Config
import pymysql
pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    models.init_app(app)
    routes.init_app(app)

    app.app_context().push()
    return app


