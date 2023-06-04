from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .articles import article as article_blueprint
    app.register_blueprint(article_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
