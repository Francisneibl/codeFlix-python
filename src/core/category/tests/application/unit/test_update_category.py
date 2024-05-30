from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.Category import Category
from unittest.mock import create_autospec


class TestUpdateCategory:

    def test_update_category_name(self):
        category = Category(
            name="Movie",
            description="Categories for series"
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, name="Series"))

        assert category.name == "Series"
        assert category.description == "Categories for series"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            name="Series",
            description="Categories for movies"
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, description="Categories for series"))

        assert category.name == "Series"
        assert category.description == "Categories for series"
        mock_repository.update.assert_called_once_with(category)

    def test_deactivate_category(self):
        category = Category(
            name="Series",
            description="Categories for movies",
            is_active=True
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, is_activate=False))

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_active_category(self):
        category = Category(
            name="Series",
            description="Categories for movies",
            is_active=False
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, is_activate=True))

        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
