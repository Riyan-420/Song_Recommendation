from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class QuestionnaireForm(FlaskForm):
    q1_personality = SelectField('How would you describe your personality?', 
                                choices=[
                                    ('introvert', 'Introverted - I prefer quiet and solitude'),
                                    ('extrovert', 'Extroverted - I enjoy social situations'),
                                    ('ambivert', 'Ambivert - I\'m somewhere in between')
                                ],
                                validators=[DataRequired()])
    
    q2_mood = SelectField('What kind of mood are you usually in?',
                         choices=[
                             ('energetic', 'Energetic and upbeat'),
                             ('relaxed', 'Calm and relaxed'),
                             ('melancholic', 'Reflective or melancholic'),
                             ('varied', 'It varies widely')
                         ],
                         validators=[DataRequired()])
    
    q3_tempo = SelectField('What music tempo do you prefer?',
                          choices=[
                              ('fast', 'Fast and upbeat'),
                              ('medium', 'Medium tempo'),
                              ('slow', 'Slow and mellow'),
                              ('varied', 'I enjoy variety')
                          ],
                          validators=[DataRequired()])
    
    q4_genres = SelectField('Which genre do you listen to most often?',
                           choices=[
                               ('pop', 'Pop'),
                               ('rock', 'Rock'),
                               ('hiphop', 'Hip Hop/Rap'),
                               ('electronic', 'Electronic/Dance'),
                               ('classical', 'Classical'),
                               ('jazz', 'Jazz'),
                               ('folk', 'Folk/Country'),
                               ('indie', 'Indie/Alternative'),
                               ('other', 'Other')
                           ],
                           validators=[DataRequired()])
    
    q5_lyrics = SelectField('How important are lyrics to you?',
                           choices=[
                               ('very', 'Very important - I focus on the message'),
                               ('somewhat', 'Somewhat important - I notice them but don\'t focus on them'),
                               ('not', 'Not important - I focus more on the sound')
                           ],
                           validators=[DataRequired()])
    
    other_info = TextAreaField('Anything else you\'d like to tell us about your music preferences?')
    
    submit = SubmitField('Get Recommendations')