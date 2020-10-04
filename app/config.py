from os import environ
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    APP_HOME = environ.get('APP_HOME')

class Auth_config:
    AUTH0_CALLBACK_URL =  environ.get('AUTH0_CALLBACK_URL')
    AUTH0_CLIENT_ID =  environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
    AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
    AUTH0_AUDIENCE = environ.get('AUTH0_AUDIENCE')
    ALGORITHM = environ.get('AUTH0_ALGORITHM')
