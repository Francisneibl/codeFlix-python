from rest_framework.test import APITestCase

from src.core.category.domain.Category import Category
from djangoproject.category_app.repository import DjangoORMCategoryRepository
# Create your tests here.


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"

        movie_category = Category(
            name="Movies",
            description="Category for movies"
        )

        series_category = Category(
            name="Series",
            description="Category for series"
        )

        repository = DjangoORMCategoryRepository()
        repository.save(movie_category)
        repository.save(series_category)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertEqual(response.data, [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active
            } for category in [movie_category, series_category]
        ])
