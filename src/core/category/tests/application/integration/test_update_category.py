from uuid import uuid4
import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.Category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Movie",
            description="Categories for series"
        )

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, name="Series"))

        edited_category = repository.get_by_id(category.id)
        assert edited_category.name == "Series"
        assert edited_category.description == "Categories for series"

    def test_update_category_description(self):
        category = Category(
            name="Movie",
            description="Categories for series"
        )

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, description="Categories for movies"))

        edited_category = repository.get_by_id(category.id)
        assert edited_category.name == "Movie"
        assert edited_category.description == "Categories for movies"

    def test_update_category_name_and_description(self):
        category = Category(
            name="Movie",
            description="Categories for movies"
        )

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, description="Categories for series", name="Series"))

        edited_category = repository.get_by_id(category.id)
        assert edited_category.name == "Series"
        assert edited_category.description == "Categories for series"

    def test_update_category_name_and_deactivate(self):
        category = Category(
            name="Movie",
            description="Categories for series",
            is_active=True
        )

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            name="Series", is_activate=False
        ))

        edited_category = repository.get_by_id(category.id)
        assert edited_category.name == "Series"
        assert edited_category.description == "Categories for series"
        assert edited_category.is_active is False

    def test_raise_exception_on_update_nonexistent_category(self):
        category = Category(
            name="Series",
            description="Categories for movies",
            is_active=False
        )

        nonexistent_id = uuid4()

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        with pytest.raises(CategoryNotFound, match=f"not found category with id = {nonexistent_id}"):
            use_case.execute(UpdateCategoryRequest(id=nonexistent_id, is_activate=True))

    def test_raise_exception_on_update_category_with_invalid_name(self):
        category = Category(
            name="Movies",
            description="Categories for movies",
            is_active=False
        )

        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository)
        with pytest.raises(ValueError, match="name cannot be empty"):
            use_case.execute(UpdateCategoryRequest(id=category.id, name=""))
