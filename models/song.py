from extensions import db

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    # Trait tags
    extraversion = db.Column(db.Integer)
    openness      = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    agreeableness    = db.Column(db.Integer)
    neuroticism      = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    mood   = db.Column(db.Integer)
    lyrics_importance = db.Column(db.Boolean)
    album_art_url = db.Column(db.String(200))
    # etc.
