from flask_migrate import Migrate

from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

