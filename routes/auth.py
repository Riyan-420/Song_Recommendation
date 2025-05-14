from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
from extensions import db
from models.user import User
from forms.login_form import LoginForm
from forms.register_form import RegistrationForm
from forms.profile_form import ProfileForm
from models.preference import Preference
from config import Config

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('recommendations.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('recommendations.home')
            flash('You have been logged in successfully!', 'success')

            # 👇 Admin redirect logic
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))  # Replace 'admin.dashboard' with the actual endpoint name

            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('recommendations.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='Register', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Check if we're in edit mode
    edit_mode = request.args.get('edit', 'false').lower() == 'true'
    
    form = ProfileForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            form.profile_pic.data.save(filepath)
            current_user.profile_pic = filename
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # Get user preferences if they exist
    preferences = Preference.query.filter_by(user_id=current_user.id).first()
    
    # Only pass the form if in edit mode
    if not edit_mode and request.method == 'GET':
        return render_template('profile.html', title='Profile', preferences=preferences, edit_mode=False)
    else:
        return render_template('profile.html', title='Profile', form=form, preferences=preferences, edit_mode=True)