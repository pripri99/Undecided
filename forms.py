import models
from flask_wtf import FlaskForm
from wtforms import *
from wtforms import validators

user_form = FlaskForm(models.User, exclude=['password'])

# Signup Form created from user_form
class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('Password',validators=[validators.Required()])