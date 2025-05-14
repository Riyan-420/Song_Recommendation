from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/musicplayer'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User
    from models.song import Song
    from models.preference import Preference
    from models.recommendation import Recommendation

    with app.app_context():
        db.create_all()

    return app
