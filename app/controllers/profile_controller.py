from flask import (
	Blueprint, render_template, json, flash, redirect, url_for, jsonify
)
import requests ,string, collections
from sqlalchemy.sql import func
from sqlalchemy import desc
from app.models.user import User
from app.models.playlist import PlayList
from app.models.artist import Artist
from app import (
	models, db
)
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
			flash ("Welcome back " + user_data['display_name'])

			return u.id

	# Registering user
	user_db = User()
	user_db.display_name = user_data['display_name']
	user_db.spotify_id = user_data['id']
	user_db.email = user_data['email']
	user_db.kind = user_data['type']
	user_db.country = user_data['country']
	user_db.followers = user_data['followers']
	user_db.product = user_data['product']
	
	db.session.add(user_db)
	db.session.commit()

	flash ("Welcome " + user_db.display_name + ", in spotify review you can see you use profile in spotify.")

	return user_db.id


def request_playlists(user_id, access_token, db_id):
	# Request the user playlists
	headers = {"Authorization": "Bearer " + access_token}
	response = requests.get("https://api.spotify.com/v1/users/" + str(user_id) + "/playlists?limit=50", headers=headers)
	playlists = response.json()
	playlists_ids = []
		
	# Removing old play list of user
	db.session.query(PlayList).filter_by(user=db_id).delete()
	db.session.commit()

	# Taking the playlists data and saving
	for playlist in playlists['items']:
		playlist_db = PlayList()
		playlist_db.playlist_id = playlist['id']
		playlist_db.name = playlist['name']
		playlist_db.url = playlist['external_urls']['spotify']
		playlist_db.image = playlist['images'][0]['url']
		playlist_db.user = db_id
		playlist_db.owner = playlist['owner']['id']

		if (playlist['public']):
			playlist_db.public = True
		else:
			playlist_db.public = False

		db.session.add(playlist_db)
		db.session.commit()
		playlists_ids.append(playlist_db.id)

	return playlists_ids


def request_artists_id(access_token, playlists_ids):
	artists_ids = []

	for playlists_id in playlists_ids:
		playlist = PlayList.query.get(playlists_id)

		headers = {"Authorization": "Bearer " + access_token}
		response = requests.get("https://api.spotify.com/v1/users/" +
			str(playlist.owner) + "/playlists/" +
			str(playlist.playlist_id) +
			"?fields=tracks.items(track(album(artists)))", headers=headers)
		tracks = response.json()	

		for track in tracks["tracks"]["items"]:
			if (track["track"]):
				artists_ids.append(track["track"]["album"]["artists"][0]["id"])
	

	# return thw list without duplicates
	return list(set(artists_ids))


def request_artists(user_id, access_token, artists_ids):
	artists_number = len(artists_ids)
	range_control = 0

	# Removing old artists associeted with user
	db.session.query(Artist).filter_by(user=user_id).delete()
	db.session.commit()

	# while artists_number > 0:
	headers = {"Authorization": "Bearer " + access_token}
	
	while artists_number > range_control:
		# Max request size
		if (artists_number > 50):
			response = requests.get("https://api.spotify.com/v1/artists?ids=" +
				str(",".join(artists_ids[range_control:(range_control + 49)])), headers=headers)
				
			range_control += 50

		else:
			response = requests.get("https://api.spotify.com/v1/artists?ids=" +
				str(artists_ids[range_control:artists_number]), headers=headers)

		artists = response.json()

		# Taking the artist data and saving
		for artist in artists['artists']:
			artist_db = Artist()
			artist_db.user = user_id
			artist_db.name = artist['name']
			artist_db.spotify_id = artist['id']
			
			if (len(artist['images']) > 0):
				artist_db.image = artist['images'][0]['url']
			else:
				artist_db.image = "https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg"

			artist_db.url = artist['external_urls']['spotify']
			artist_db.popularity = artist['popularity']
			artist_db.genres = artist['genres']

			db.session.add(artist_db)
			db.session.commit()


def user_score(user_id):
	artists = db.session.query(Artist).filter_by(user=user_id).all()
	user = db.session.query(User).get(user_id)
	score = 0

	for artist in artists:
		score += artist.popularity

	score /= len(artists)

	user.score = score;
	db.session.add(user)
	db.session.commit()

	return score

@blueprint.route('/playlists/<user_id>')
def get_playlists(user_id):
	playlists = [dict(i) for i in db.session.query(PlayList).filter_by(user=user_id).all()]

	return jsonify(playlists=playlists), 200

@blueprint.route('/styles/<user_id>')
def get_styles(user_id):
	artists = db.session.query(Artist).filter_by(user=user_id).all()

	all_genres = []

	# Geting all genres
	for artist in artists:
		for genres in artist.genres.split(','):
			genres_str = str(genres)
			all_genres.append(genres_str.translate(None, string.punctuation))
	
	all_genres_clean = filter(None, all_genres)
	counter = collections.Counter(all_genres_clean)
	counter_sorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)

	json_data = [{'name' : x[0],'value' : x[1]}  for x in counter_sorted]

	return jsonify(json_data=json_data), 200


@blueprint.route('/artists/top10/<user_id>')
def get_top10(user_id):
	artists = [dict(i) for i in db.session.query(Artist).filter_by(user=user_id).order_by(desc("popularity")).limit(10).all()]

	return jsonify(json_data=artists), 200


@blueprint.route('/<user>/<token>')
def user_profile(user, token):
	user_data = json.loads(user)

	user_id = register(user_data)

	# playlists_ids = request_playlists(user_data['id'], token, user_id)

	# artists_ids = request_artists_id(token, playlists_ids)

	# request_artists (user_id, token, artists_ids)

	score = user_score(user_id)

	get_top10(user_id)

	return render_template('profile/index.html', user=user_data, score=score, user_id=user_id)


@blueprint.route('/charts')
def charts():
	return render_template('profile/charts.html')
