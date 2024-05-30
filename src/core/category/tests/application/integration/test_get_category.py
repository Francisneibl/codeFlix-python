from uuid import uuid4, UUID

import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.get_category import GetCategory, GetCategoryResponse, GetCategoryRequest
from src.core.category.domain.Category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_find_category_by_id(self):
        category_movies = Category(name="Movie")
        category_series = Category(name="Series")
        repository = InMemoryCategoryRepository([category_movies, category_series])

        use_case = GetCategory(repository)
        request = GetCategoryRequest(id=category_movies.id)
        response = use_case.execute(request)

        assert isinstance(response, GetCategoryResponse)
        assert isinstance(response.id, UUID)
        assert request.id == response.id
        assert response.name == category_movies.name

    def test_raise_exception_when_not_found_category(self):
        repository = InMemoryCategoryRepository()

        use_case = GetCategory(repository)
        request = GetCategoryRequest(id=uuid4())
        with pytest.raises(CategoryNotFound, match=f"not found category with id = {request.id}"):
            use_case.execute(request)
