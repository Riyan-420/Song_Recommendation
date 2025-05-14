from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # <== ADD THIS LINE
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'