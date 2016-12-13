from test_base import BaseTestCase


class HomeControllerTests(BaseTestCase):

	def test_should_respond_ok_to_home_path(self):
		response = self.client.get("/")
		self.assert_200(response)

	def test_shouuld_responde_to_about(self):
		response = self.client.get("/about")
		self.assert_200(response)