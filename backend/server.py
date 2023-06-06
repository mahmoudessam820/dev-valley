import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import Users, Articles, Comments, Premissions

app = create_app(os.getenv('APP_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Users=Users, Articles=Articles, Comments=Comments,
                Permissions=Premissions)
