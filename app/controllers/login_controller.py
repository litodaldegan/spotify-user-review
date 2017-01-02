from flask import Blueprint, render_template, url_for, request, session, redirect, json
from flask_oauthlib.client import OAuth, OAuthException
from config import Config

blueprint = Blueprint('login_controller', __name__, url_prefix='/login')

blueprint.secret_key = Config.SECRET_KEY

oauth = OAuth(blueprint)

spotify = oauth.remote_app('spotify',
	consumer_key=Config.SPOTIFY_APP_ID,
	consumer_secret=Config.SPOTIFY_APP_SECRET,
	request_token_params={'scope': ['user-read-email', 'playlist-read-private', 'user-read-private']},
	base_url='https://accounts.spotify.com',
	request_token_url=None,
	access_token_url='/api/token',
	authorize_url='https://accounts.spotify.com/authorize'
)


@blueprint.route('')
def login():
	callback = url_for(
		'login_controller.spotify_authorized',
		_external=True
	)
	return spotify.authorize(callback=callback)


@blueprint.route('/authorized')
def spotify_authorized():
	resp = spotify.authorized_response()
	if resp is None:
		return 'Access denied: reason={0} error={1}'.format(
			request.args['error_reason'],
			request.args['error_description']
		)

	session['oauth_token'] = (resp['access_token'], '')
	me = spotify.get('https://api.spotify.com/v1/me')

	user = {
		'display_name': me.data['display_name'],
		'email': me.data['email'],
		'country': me.data['country'],
		'followers': me.data['followers']['total'],
		'id': me.data['id'],
		'type': me.data['type'],
		'product': me.data['product'],
		'token': session['oauth_token']
	}

	user_json = json.dumps(user)

	return redirect(url_for('profile_controller.user_profile', user=user_json, token=resp['access_token']))


@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')