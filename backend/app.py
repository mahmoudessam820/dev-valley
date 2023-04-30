from views.home import (home_bp)
import os

from flask import Flask
from flask_migrate import Migrate

from models.model import db, User, Article

#! Instantiation Migrate
migrate: Migrate = Migrate()


def create_app() -> Flask:

    #! App Configurations
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ.get(
        'APP_SETTINGS', 'config.DevelopmentConfig'))
    db.init_app(app)

    #! Migrate Configurations
    migrate.init_app(app, db)

    app.register_blueprint(home_bp)

    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
    # app.run(host='0000000', port=5000)
    # app.run(host='0000000', port=5000, debug=True)
    # app.run(host='0000000', port=5000, debug=True, ssl_context='adhoc')
    # app.run(host='0000000', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host='0000000', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'), use_reloader=False)
    # app.run(host='0000000', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'), use_reloader=False, threaded=True)
