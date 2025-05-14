from flask import Flask
from flask_migrate import Migrate
from extensions import db
from app import create_app
from models import user, preference, recommendation  # Make sure __init__.py exists in models folder

app = create_app()
migrate = Migrate(app, db)

app.app_context().push()
