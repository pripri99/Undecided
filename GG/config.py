import os
from dotenv import load_dotenv
load_dotenv()

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True


#'SECRET_KEY = 'key-goes-here'
SQLALCHEMY_DATABASE_URI= 'sqlite:///db.sqlite'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = "password"
