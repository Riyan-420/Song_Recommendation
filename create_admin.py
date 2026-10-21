"""Create the initial admin user.

Credentials are read from ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD
(environment or .env). Usage: python create_admin.py
"""
import os
import sys

from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models.user import User

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL')
password = os.environ.get('ADMIN_PASSWORD')

if not email or not password:
    sys.exit('Set ADMIN_EMAIL and ADMIN_PASSWORD (and optionally ADMIN_USERNAME) first.')

app = create_app()

with app.app_context():
    if User.query.filter_by(email=email).first():
        print("Admin already exists.")
    else:
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully.")
