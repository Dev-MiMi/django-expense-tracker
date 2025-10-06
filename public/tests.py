from django.test import SimpleTestCase

# Create your tests here.


class GetStartedTest(SimpleTestCase):
    def test_getstarted_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
