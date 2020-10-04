from flask import Blueprint, session, redirect
from flask_cors import CORS
from ..config import Auth_config
from .auth import auth0
from six.moves.urllib.parse import urlencode
import json
from os import environ

auth = Blueprint('auth', __name__)

@auth.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'token': token['access_token']
    }
    return redirect('/')


@auth.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=Auth_config.AUTH0_CALLBACK_URL, audience=Auth_config.AUTH0_AUDIENCE)


@auth.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': environ.get(
        'APP_HOME'), 'client_id': 'KLgbm50Cz09HTyvVQy64nfQz7SUSZCXd'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))