from test_base import BaseTestCase


class ProfileApiTests(BaseTestCase):

	def test_should_respond_ok_to_profile_path(self):
		response = self.client.get("/")