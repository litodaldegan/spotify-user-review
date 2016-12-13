from flask import (
	Blueprint, render_template, json, flash, redirect, url_for
)
import requests
from app.models.user import User
from app.models.playlist import PlayList
from app import models
from app import db
from config import Config

blueprint = Blueprint('profile_controller', __name__, url_prefix='/profile')

@blueprint.route('')
def profile():
	return "None user given"


def register(user_data):
	# If user don't have a display name
	if (not user_data['display_name']):
		user_data['display_name'] = user_data['id']

	users = User.query.all()

	for u in users:

		# Checking if the user is registered
		if u.spotify_id == user_data['id']:
			flash ("Welcome back" + user_data['display_name'])

			return u.id

	# Registering user
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

	return userDB.id


def get_playlists(user_id, access_token, db_id):
	# Request the user playlists
	headers = {"Authorization": "Bearer " + access_token}
	response = requests.get("https://api.spotify.com/v1/users/" + str(user_id) + "/playlists?limit=50", headers=headers)
	playlists = response.json()
	playlistsIDs = []
		
	# Removing old play list of user
	db.session.query(PlayList).filter_by(user=db_id).delete()
	db.session.commit()

	# Taking the playlists data and saving
	for playlist in playlists['items']:
		playlistDB = PlayList()
		playlistDB.playlist_id = playlist['id']
		playlistDB.name = playlist['name']
		playlistDB.url = playlist['external_urls']['spotify']
		playlistDB.image = playlist['images'][0]['url']
		playlistDB.user = db_id
		playlistDB.owner = playlist['owner']['id']

		if (playlist['public']):
			playlistDB.public = True
		else:
			playlistDB.public = False

		db.session.add(playlistDB)
		db.session.commit()
		playlistsIDs.append(playlistDB.id)

	user = db.session.query(User).filter_by(spotify_id = "test").first()

	return playlistsIDs


def get_tracks(user_id, access_token, playlistsIDs):
	artistsIDS = []

	for playlistsID in playlistsIDs:
		playlist = PlayList.query.get(playlistsID)

		headers = {"Authorization": "Bearer " + access_token}
		response = requests.get("https://api.spotify.com/v1/users/" +
			str(playlist.owner) + "/playlists/" +
			str(playlist.playlist_id) +
			"?fields=tracks.items(track(album(artists)))", headers=headers)
		tracks = response.json()	

		for track in tracks["tracks"]["items"]:
			artistsIDS.append(track["track"]["album"]["artists"][0]["id"])

		import pdb; pdb.set_trace()
	
	return artistsIDS

	# tracks["tracks"]["items"][0]["track"]["album"]["artists"][0]["id"]


@blueprint.route('/<user>/<token>')
def user_profile(user, token):
	user_data = json.loads(user)

	db_id = register(user_data)

	pls_ids = get_playlists(user_data['id'], token, db_id)

	get_tracks(user_data['id'], token, pls_ids)

	return render_template('profile/index.html', user=user_data)


@blueprint.route('/charts')
def charts():
	return render_template('profile/charts.html')
