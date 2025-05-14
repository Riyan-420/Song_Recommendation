from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash
from app import create_app

# Your admin credentials
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@musicmind.org"
ADMIN_PASSWORD = "adminn"

app = create_app()

with app.app_context():
    existing_admin = User.query.filter_by(email=ADMIN_EMAIL).first()
    
    if existing_admin:
        print("Admin already exists.")
    else:
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully.")
