from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.preference import Preference
from models.recommendation import Recommendation
from models.song import Song

recommendations = Blueprint('recommendations', __name__)

@recommendations.route('/home')
@login_required
def home():
    # Get a few recent recommendations for the user (if any)
    user_recommendations = Recommendation.query.filter_by(user_id=current_user.id).limit(3).all()
    return render_template('dashboard_home.html', title='Dashboard', recommendations=user_recommendations)

@recommendations.route('/dashboard')
@login_required
def dashboard():
    # Get user recommendations
    user_recommendations = Recommendation.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Recommendations', recommendations=user_recommendations)

@recommendations.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    # We'll keep this route to match the navigation, but for now
    # it will just render your existing questionnaire template
    return render_template('questionnaire.html', title='Personality Questionnaire')

# This is where your form in questionnaire.html should post to
@recommendations.route('/save_preferences', methods=['POST'])
@login_required
def save_preferences():
    # Check if the request method is POST
    # Map form value to DB genre
    GENRE_MAP = {
        'pop': 'Pop', 'rock': 'Rock', 'hip_hop': 'Hip-Hop',
        'electronic': 'Electronic', 'classical': 'Classical',
        'jazz': 'Jazz', 'country': 'Country',
        'r_and_b': 'R&B', 'indie': 'Indie', 'metal': 'Metal'
    }
    raw_genre = request.form.get('favorite_genre')
    favorite_genre = GENRE_MAP.get(raw_genre, raw_genre)

    if request.method == 'POST':
        # Extract all the form data from request.form
        extraversion = request.form.get('extraversion')
        openness = request.form.get('openness')
        conscientiousness = request.form.get('conscientiousness')
        agreeableness = request.form.get('agreeableness')
        neuroticism = request.form.get('neuroticism')
        favorite_genre = request.form.get('favorite_genre')
        energy_preference = request.form.get('energy_preference')
        mood_preference = request.form.get('mood_preference')
        lyrics_importance = request.form.get('lyrics_importance', '3')  # Default to neutral if not provided
        cultural_openness = request.form.get('cultural_openness', '3')  # Default to neutral if not provided
        
        # Convert personality traits to a single type for storage
        personality_scores = {
            'extraversion': int(extraversion) if extraversion else 3,
            'openness': int(openness) if openness else 3,
            'conscientiousness': int(conscientiousness) if conscientiousness else 3,
            'agreeableness': int(agreeableness) if agreeableness else 3,
            'neuroticism': int(neuroticism) if neuroticism else 3
        }
        
        # Determine overall personality type based on highest score
        max_trait = max(personality_scores, key=personality_scores.get)
        personality_type = max_trait
        
        # Save to preferences
        preference = Preference.query.filter_by(user_id=current_user.id).first()

        if not preference:
            preference = Preference(
                user_id=current_user.id,
                personality_type=personality_type,
                genre_preference=favorite_genre,      # if you’ve kept this field
                tempo_preference=int(request.form.get('tempo_preference', 3)),
                mood=int(mood_preference),
                openness=int(openness),
                conscientiousness=int(conscientiousness),
                extraversion=int(extraversion),
                agreeableness=int(agreeableness),
                neuroticism=int(neuroticism),
                energy_preference=int(energy_preference),
                mood_preference=int(mood_preference),
                vocals_preference=(request.form.get('vocals') == '1'),
                favorite_genre=favorite_genre
            )
            db.session.add(preference)
        else:
            preference.personality_type = personality_type
            preference.genre_preference = favorite_genre
            preference.tempo_preference = int(request.form.get('tempo_preference', 3))
            preference.mood = int(mood_preference)
            preference.openness = int(openness)
            preference.conscientiousness = int(conscientiousness)
            preference.extraversion = int(extraversion)
            preference.agreeableness = int(agreeableness)
            preference.neuroticism = int(neuroticism)
            preference.energy_preference = int(energy_preference)
            preference.mood_preference = int(mood_preference)
            preference.vocals_preference = (request.form.get('vocals') == '1')
            preference.favorite_genre = favorite_genre

        # Commit should happen in both cases
        db.session.commit()

        # Now generate recommendations
        generate_recommendations(current_user.id)

        flash('Your preferences have been saved! Check out your recommendations.', 'success')
        return redirect(url_for('recommendations.dashboard'))

    # Fallback (non-POST)
    return redirect(url_for('recommendations.questionnaire'))

@recommendations.route('/recommendations/<int:recommendation_id>/rate', methods=['POST'])
@login_required
def rate_recommendation(recommendation_id):
    rating = request.form.get('rating')
    
    if not rating:
        flash('Please provide a rating.', 'danger')
        return redirect(url_for('recommendations.dashboard'))
    
    recommendation = Recommendation.query.get_or_404(recommendation_id)
    
    if recommendation.user_id != current_user.id:
        flash('You can only rate your own recommendations.', 'danger')
        return redirect(url_for('recommendations.dashboard'))
    
    recommendation.user_rating = int(rating)
    db.session.commit()
    
    flash('Thank you for rating this recommendation!', 'success')
    return redirect(url_for('recommendations.dashboard'))

def generate_recommendations(user_id):
    pref = Preference.query.filter_by(user_id=user_id).first()
    if not pref: 
        return
    Recommendation.query.filter_by(user_id=user_id).delete()
    
    query = Song.query
    if pref.favorite_genre:
        query = query.filter(Song.genre.ilike(pref.favorite_genre))

    query = query.filter(
        Song.extraversion.between(pref.extraversion-1, pref.extraversion+1),
        Song.energy.between(pref.energy_preference-1, pref.energy_preference+1)
    )

    songs = query.limit(10).all()
    for song in songs:
        add_recommendation(
            user_id,
            song.title,
            song.artist,
            song.album,
            song.genre,
            song.album_art_url,
            song.year
        )

    db.session.commit()



def add_recommendation(user_id, title, artist, album, genre, album_art_url, year):
    rec = Recommendation(
        user_id=user_id,
        song_title=title,
        artist=artist,
        album=album,
        genre=genre,
        album_art_url=album_art_url,
        year=year
    )
    db.session.add(rec)


@recommendations.route('/check_recs')
@login_required
def check_recs():
    count = Recommendation.query.filter_by(user_id=current_user.id).count()
    return f"You have {count} recommendations"


@recommendations.route('/check_genre_filter')
@login_required
def check_genre_filter():
    pref = Preference.query.filter_by(user_id=current_user.id).first()
    if not pref or not pref.favorite_genre:
        return "No favorite_genre set!"
    # Use ilike for case-insensitive matching (PostgreSQL specific)
    count = Song.query.filter(Song.genre.ilike(pref.favorite_genre)).count()
    return f"{count} songs match your favorite_genre = {pref.favorite_genre}"


@recommendations.route('/check_full_filter')
@login_required
def check_full_filter():
    pref = Preference.query.filter_by(user_id=current_user.id).first()
    if not pref:
        return "No preferences set!"
    
    # Replicate the filters from generate_recommendations
    query = Song.query

    if pref.favorite_genre:
        query = query.filter(Song.genre.ilike(pref.favorite_genre))

    query = query.filter(
        Song.extraversion.between(pref.extraversion-1, pref.extraversion+1),
        Song.energy.between(pref.energy_preference-1, pref.energy_preference+1)
    )

    count = query.count()
    return (
        f"After genre & extraversion±1 & energy±1 filters: {count} matches "
        f"(extraversion={pref.extraversion}, energy={pref.energy_preference})"
    )
