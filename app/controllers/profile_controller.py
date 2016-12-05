from flask import Blueprint, render_template

blueprint = Blueprint('profile_controller', __name__, url_prefix='/profile')

@blueprint.route("/")
def profile():
	return render_template('profile/index.html')


@blueprint.route("/charts")
def charts():
	return render_template('profile/charts.html')