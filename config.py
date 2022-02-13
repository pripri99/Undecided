import os
from dotenv import load_dotenv
load_dotenv()

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
MONGODB_SETTINGS  =  {'HOST':os.getenv('MONGOLAB'),'DB': 'FlaskLogin'}
SECRET_KEY = os.getenv('SECRET_KEYDB')
#MONGODB_SETTINGS = {'DB': 'Cluster0', "host":os.getenv('MONGOLAB_URI')}
#SECRET_KEY = os.getenv('SECRET_KEYDB')