import pytest
from djangoproject.category_app.repository import DjangoORMCategoryRepository
from rest_framework.test import APIClient

from src.core.category.domain.Category import Category


# Create your tests here.


@pytest.mark.django_db
class TestCategoryAPI():

    @pytest.fixture
    def movie_category(self) -> Category:
        return Category(
            name="Movies",
            description="Category for movies"
        )

    @pytest.fixture
    def series_category(self) -> Category:
        return Category(
            name="Movies",
            description="Category for movies"
        )

    @pytest.fixture
    def repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_list_categories(self, movie_category, series_category, repository):
        url = "/api/categories/"

        repository.save(movie_category)
        repository.save(series_category)

        response = APIClient().get(url)

        assert response.status_code == 200
        assert response.data == [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active
            } for category in [movie_category, series_category]
        ]
