from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DecimalField, IntegerField, FileField, PasswordField, SubmitField, validators
from models import Status, TipoDeProduto

class AdminForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25), 
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=30),
        validators.EqualTo('password2', message='Passwords must match'),
    ])
    password2 = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=30),
    ])
    submit = SubmitField("Confirmar")

