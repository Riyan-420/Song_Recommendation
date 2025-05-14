from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[Optional()])
    album = StringField('Album', validators=[Optional()])
    genre = StringField('Genre', validators=[Optional()])
    year = IntegerField('Year', validators=[Optional()])
    extraversion = IntegerField('Extraversion', validators=[Optional()])
    openness = IntegerField('Openness', validators=[Optional()])
    conscientiousness = IntegerField('Conscientiousness', validators=[Optional()])
    agreeableness = IntegerField('Agreeableness', validators=[Optional()])
    neuroticism = IntegerField('Neuroticism', validators=[Optional()])
    energy = IntegerField('Energy', validators=[Optional()])
    mood = IntegerField('Mood', validators=[Optional()])
    lyrics_importance = BooleanField('Lyrics Importance', validators=[Optional()])
    album_art_url = StringField('Album Art URL', validators=[Optional()])
    submit = SubmitField('Save Song') 