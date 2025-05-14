from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NotificationForm(FlaskForm):
    message = StringField('Notification Message', validators=[DataRequired()])
    submit = SubmitField('Send Notification') 