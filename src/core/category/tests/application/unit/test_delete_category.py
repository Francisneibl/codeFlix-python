import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.Category import Category
from unittest.mock import create_autospec


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Movie",
            description="Category for movies"
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_raise_exception(self):
        category = Category(
            name="Movie",
            description="Category for movies"
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_repository)

        with pytest.raises(CategoryNotFound, match=f"not found category with id = {id}"):
            use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_not_called()
