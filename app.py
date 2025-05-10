
from flask import Flask, render_template, url_for, redirect
from flask_login import current_user
from config import Config
from extensions import db, login_manager, migrate
from routes.admin import admin_bp

import os

from models.user import User
from models.preference import Preference
from models.recommendation import Recommendation

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(admin_bp)
    # Create required directories if they don't exist
    uploads_dir = os.path.join(app.static_folder, 'uploads')
    img_dir = os.path.join(app.static_folder, 'img')
    
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    # Create a default avatar image if it doesn't exist
    default_avatar_path = os.path.join(img_dir, 'default-avatar.jpg')
    if not os.path.exists(default_avatar_path):
        # Create a placeholder text file to notify user
        with open(os.path.join(img_dir, 'default-avatar-missing.txt'), 'w') as f:
            f.write("Please add a default-avatar.jpg image in this directory for user profile defaults")
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from routes.auth import auth as auth_blueprint
    from routes.recommendations import recommendations as recommendations_blueprint
    
    # Register WITHOUT URL prefixes
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(recommendations_blueprint)
    
    # Create all database tables within app context
    with app.app_context():
        db.create_all()
    
    # Add root route for home page
    @app.route('/')
    def index():
        # If user is already logged in, redirect to dashboard
        if current_user.is_authenticated:
            return redirect(url_for('recommendations.home'))
        # Otherwise show landing page
        return render_template('index.html', title='Home')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)