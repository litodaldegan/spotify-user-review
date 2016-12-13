from test_base import BaseTestCase

class LoginControllerTests(BaseTestCase):

	def test_should_redirect_to_login(self):
		response = self.client.get("/login")
		self.assertEqual(response.status_code, 302)


	def test_should_not_authorized(self):
		response = self.client.get("/login/authorized")
		self.assertEqual(response.status_code, 400)