from rest_framework.test import APITestCase
# Create your tests here.


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
