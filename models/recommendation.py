from extensions import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Song information
    song_title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    album_art_url = db.Column(db.String(200))
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    
    # Recommendation metadata
    recommendation_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_rating = db.Column(db.Integer, nullable=True)  # 1-5 rating from user
    listened = db.Column(db.Boolean, default=False)