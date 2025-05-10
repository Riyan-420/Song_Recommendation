from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from models.preference import Preference
from models.user import User
from config import Config

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def view_profile():
    # Get user preferences if they exist
    preferences = Preference.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', preferences=preferences)

@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Update username if provided
        username = request.form.get('username')
        if username and username != current_user.username:
            # Check if username already exists
            if User.query.filter_by(username=username).first() is not None:
                flash('Username already exists.')
                return redirect(url_for('profile.edit_profile'))
            current_user.username = username
        
        # Handle profile picture upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Create a unique filename with user id
                file_ext = os.path.splitext(filename)[1]
                new_filename = f"user_{current_user.id}{file_ext}"
                file_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)
                file.save(file_path)
                
                # Update user's profile pic in database
                current_user.profile_pic = new_filename
        
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile_edit.html')

@profile.route('/questionnaire')
@login_required
def questionnaire():
    return render_template('questionnaire.html')

@profile.route('/save_preferences', methods=['POST'])
@login_required
def save_preferences():
    # Get form data for personality traits
    openness = int(request.form.get('openness', 3))
    conscientiousness = int(request.form.get('conscientiousness', 3))
    extraversion = int(request.form.get('extraversion', 3))
    agreeableness = int(request.form.get('agreeableness', 3))
    neuroticism = int(request.form.get('neuroticism', 3))
    
    # Get form data for music preferences
    favorite_genre = request.form.get('favorite_genre')
    energy_preference = int(request.form.get('energy_preference', 3))
    mood_preference = int(request.form.get('mood_preference', 3))
    tempo_preference = int(request.form.get('tempo_preference', 3))
    vocals_preference = request.form.get('vocals_preference') == 'true'
    
    # Check if preferences already exist
    preferences = Preference.query.filter_by(user_id=current_user.id).first()
    
    if preferences:
        # Update existing preferences
        preferences.openness = openness
        preferences.conscientiousness = conscientiousness
        preferences.extraversion = extraversion
        preferences.agreeableness = agreeableness
        preferences.neuroticism = neuroticism
        preferences.favorite_genre = favorite_genre
        preferences.energy_preference = energy_preference
        preferences.mood_preference = mood_preference
        preferences.tempo_preference = tempo_preference
        preferences.vocals_preference = vocals_preference
    else:
        # Create new preferences
        preferences = Preference(
            user_id=current_user.id,
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
            favorite_genre=favorite_genre,
            energy_preference=energy_preference,
            mood_preference=mood_preference,
            tempo_preference=tempo_preference,
            vocals_preference=vocals_preference
        )
        db.session.add(preferences)
    
    db.session.commit()
    flash('Your preferences have been saved.')
    
    # Redirect to recommendations
    return redirect(url_for('recommendations.view_recommendations'))