from views.feed import feed_bp
from auth.sign_in import sign_in_bp
from auth.log_in import login_bp
from auth.log_out import logout_bp
import os

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from models.model import db, Users, Articles

#! Instantiation Classes
migrate: Migrate = Migrate()
login_manager: LoginManager = LoginManager()


def create_app() -> Flask:

    #! App Configurations
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ.get(
        'APP_SETTINGS', 'config.DevelopmentConfig'))
    db.init_app(app)

    #! Migrate Configurations
    migrate.init_app(app, db)

    #! Login Manager Configurations
    login_manager.init_app(app)
    login_manager.login_view = 'login_bp.login'

    @login_manager.user_loader
    def load_user(user_id: str) -> None:
        return Users.query.get(int(user_id))

    app.register_blueprint(feed_bp)
    app.register_blueprint(sign_in_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)

    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
