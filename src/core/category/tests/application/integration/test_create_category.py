from uuid import UUID

import pytest

from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse, \
    InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Movie", description="Description for movie category", is_active=True
        )
        response = use_case.execute(request)

        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        saved_category = repository.categories[0]
        assert saved_category.id == response.id
        assert saved_category.name == request.name
        assert saved_category.description == request.description
        assert saved_category.is_active is True

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name=""
        )

        with pytest.raises(InvalidCategoryData, match="name cannot be empty"):
            use_case.execute(request)

        assert len(repository.categories) == 0
