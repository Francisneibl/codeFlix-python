from unittest.mock import create_autospec
from uuid import uuid4, UUID

import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.get_category import GetCategory, GetCategoryResponse, GetCategoryRequest
from src.core.category.domain.Category import Category


class TestGetCategory:
    def test_find_category_by_id(self):
        category = Category(name="Movie")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(mock_repository)
        request = GetCategoryRequest(id=category.id)
        response = use_case.execute(request)

        assert isinstance(response, GetCategoryResponse)
        assert isinstance(response.id, UUID)
        assert request.id == response.id
        assert mock_repository.get_by_id.called

    def test_raise_exception_when_not_found_category(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(mock_repository)
        request = GetCategoryRequest(id=uuid4())
        with pytest.raises(CategoryNotFound, match=f"not found category with id = {request.id}"):
            use_case.execute(request)
