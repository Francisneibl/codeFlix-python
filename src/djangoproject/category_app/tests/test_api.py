from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from src.core.category.domain.Category import Category
from ..repository import DjangoORMCategoryRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(
        name="Movies",
        description="Category for movies"
    )


@pytest.fixture
def series_category() -> Category:
    return Category(
        name="Series",
        description="Category for series"
    )


@pytest.fixture
def repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListCategory:

    def test_list_categories(self, movie_category, series_category, repository):
        url = "/api/categories/"

        repository.save(movie_category)
        repository.save(series_category)

        response = APIClient().get(url)

        assert response.status_code == 200
        assert response.data == {
            "data": [
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active
                } for category in [movie_category, series_category]
            ]}


@pytest.mark.django_db
class TestRetrieveCategory:
    def test_return_400_when_send_invalid_id(self):
        url = "/api/categories/1234/"

        response = APIClient().get(url)

        assert response.status_code == 400

    def test_retrieve_category_by_id(self, movie_category, series_category, repository):
        repository.save(movie_category)
        repository.save(series_category)

        url = f"/api/categories/{series_category.id}/"

        response = APIClient().get(url)

        assert response.status_code == 200
        assert response.data == {
            "data":
                {
                    "id": str(series_category.id),
                    "name": series_category.name,
                    "description": series_category.description,
                    "is_active": series_category.is_active
                }
        }

    def test_return_404_status_when_not_round_category(self):
        url = f"/api/categories/{uuid4()}/"

        response = APIClient().get(url)

        assert response.status_code == 404
