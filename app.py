from flask import Flask, render_template, url_for, redirect
from flask_login import current_user
from config import Config
from extensions import db, login_manager
import os

# Import models (after extensions)
from models.user import User
from models.preference import Preference
from models.recommendation import Recommendation

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    uploads_dir = os.path.join(app.static_folder, 'uploads')
    img_dir = os.path.join(app.static_folder, 'img')
    
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    

    default_avatar_path = os.path.join(img_dir, 'default-avatar.jpg')
    if not os.path.exists(default_avatar_path):
        # Create a placeholder text file to notify user
        with open(os.path.join(img_dir, 'default-avatar-missing.txt'), 'w') as f:
            f.write("Please add a default-avatar.jpg image in this directory for user profile defaults")
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from routes.auth import auth as auth_blueprint
    from routes.recommendations import recommendations as recommendations_blueprint
    from routes.main import main as main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(recommendations_blueprint)
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
