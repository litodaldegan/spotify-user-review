from test_base import BaseTestCase
from app import db
from app.models.user import User
from app.controllers.profile_controller import register

class ProfileApiTests(BaseTestCase):


	def test_should_respond_ok_to_profile_path(self):
		response = self.client.get("/profile")
		self.assert_200(response)


	def test_should_register_user(self):
		db.session.query(User).filter_by(display_name="test").delete()
		db.session.commit()

		user_data = {
			'display_name': "test",
			'spotify_id': "test",
			'email': "test",
			'kind': "test",
			'country': "test",
			'followers': 0,
			'product': "test",
			'id': "test",
			'type': "test"
		}
		
		response = register(user_data)
		user = db.session.query(User).filter_by(spotify_id = "test").first()

		self.assertEqual(response,user.id) 


	def test_json_should_have_ALL_columns(self):
		# response = self.client.get("/api/product/")
		# assert "columns" in response.json
		# assert "data" in response.json
