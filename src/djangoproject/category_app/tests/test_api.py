from uuid import uuid4, UUID

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


@pytest.mark.django_db
class TestCreateCategory:
    def test_when_receive_invalid_data_return_400(self):
        url = '/api/categories/'
        response = APIClient().post(url, data={"description": "description for category"})

        assert response.status_code == 400

        response = APIClient().post(url, data={"name": "a" * 300, "description": "description for category"})

        assert response.status_code == 400

    def test_when_receive_valid_data_return_201_and_id(self, repository: DjangoORMCategoryRepository):
        url = '/api/categories/'
        response = APIClient().post(url, data={"name": "Created category", "description": "description for category"})
        created_category_id = UUID(response.data["id"])

        assert response.status_code == 201
        assert repository.get_by_id(created_category_id).id is not None


@pytest.mark.django_db
class TestUpdateCategory:
    def test_when_receive_invalid_data_return_400(self):
        url = f"/api/categories/12345/"
        response = APIClient().put(url, data={
            "name": "",

        })

        assert response.status_code == 400
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "description": ["This field is required."],
            "is_active": ["This field is required."]
        }

    def test_when_not_found_category_return_404(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(url, data={
            "name": "Test",
            "description": "description test",
            "is_active": False

        })

        assert response.status_code == 404

    def test_when_receive_valid_data_then_update_category_and_return_204(
            self,
            movie_category: Category,
            repository: DjangoORMCategoryRepository
    ):
        repository.save(movie_category)

        url = f"/api/categories/{movie_category.id}/"
        response = APIClient().put(url, data={
            "name": "Name edited",
            "description": "Description edited",
            "is_active": False
        })

        assert response.status_code == 204


@pytest.mark.django_db
class TestDeleteCategory:
    def test_when_id_is_invalid_then_return_400(self):
        url = "/api/categories/1234/"
        response = APIClient().delete(url)

        assert response.status_code == 400

    def test_when_category_does_exist_then_return_204(self, movie_category, repository):
        repository.save(movie_category)

        url = f"/api/categories/{movie_category.id}/"
        response = APIClient().delete(url)

        assert response.status_code == 204
        assert len(repository.list()) == 0
        assert repository.get_by_id(id=movie_category.id) is None

    def test_when_category_does_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == 404