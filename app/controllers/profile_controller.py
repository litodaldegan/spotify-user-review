from flask import Blueprint, render_template, json

blueprint = Blueprint('profile_controller', __name__, url_prefix='/profile')

@blueprint.route('')
def profile():
	return render_template('profile/index.html')

@blueprint.route('/<user>')
def user_profile(user):
	user_data = json.loads(user)

	return render_template('profile/index.html', user=user_data)


@blueprint.route('/charts')
def charts():
	return render_template('profile/charts.html')