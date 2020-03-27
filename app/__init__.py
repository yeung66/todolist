from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from config import DevelopmentConfiguration

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfiguration)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as blue_print
    app.register_blueprint(blue_print)

    return app

