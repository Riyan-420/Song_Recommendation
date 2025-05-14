from extensions import db
from datetime import datetime

class Preference(db.Model):
    __tablename__ = 'preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Big 5 Traits (1-5 scale)
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    neuroticism = db.Column(db.Integer)

    # Music preferences
    favorite_genre = db.Column(db.String(50))
    energy_preference = db.Column(db.Integer)
    mood_preference = db.Column(db.Integer)
    tempo_preference = db.Column(db.Integer)
    vocals_preference = db.Column(db.Boolean)

    # New fields you're trying to use
    personality_type = db.Column(db.String(50))
    genre_preference = db.Column(db.String(50))  # Redundant but your code uses it
    mood = db.Column(db.Integer)

    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
