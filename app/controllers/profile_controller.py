from flask import (
	Blueprint, render_template, json, flash
)
import requests
from app.models.user import User
from app import models
from app import db
from config import Config

blueprint = Blueprint('profile_controller', __name__, url_prefix='/profile')

@blueprint.route('')
def profile():
	return render_template('profile/index.html')


def register(user_data):
	# If user don't have a display name
	if (not user_data['display_name']):
		user_data['display_name'] = user_data['id']

	users = User.query.all()

	for u in users:

		# Checking if the user is registered
		if u.spotify_id != user_data['id']:
			userDB = User()
			userDB.display_name = user_data['display_name']
			userDB.spotify_id = user_data['id']
			userDB.email = user_data['email']
			userDB.kind = user_data['type']
			userDB.country = user_data['country']
			userDB.followers = user_data['followers']
			userDB.product = user_data['product']
			
			db.session.add(userDB)
			db.session.commit()

			flash ("Welcome " + userDB.display_name + ", in spotify review you can see you use profile in spotify.")

			return

	flash ("Welcome back" + user_data['display_name'])


def get_playlists(user_id, access_token):
	headers = {"Authorization": "Bearer " + access_token}
	response = requests.get("https://api.spotify.com/v1/users/" + str(user_id) + "/playlists?limit=50", headers=headers)
	playlists = response.json()

	import pdb; pdb.set_trace()
	# playlists['items'][0]['name']

	return playlists


@blueprint.route('/<user>/<token>')
def user_profile(user, token):
	user_data = json.loads(user)

	register(user_data)

	get_playlists(user_data['id'], token)

	return render_template('profile/index.html', user=user_data)


@blueprint.route('/charts')
def charts():
	return render_template('profile/charts.html')
