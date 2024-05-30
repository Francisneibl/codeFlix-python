import pytest

from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.Category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        movie_category = Category(
            name="Movie",
            description="Category for movies"
        )

        series_category = Category(
            name="Series",
            description="Category for series"
        )

        repository = InMemoryCategoryRepository([movie_category, series_category])

        assert repository.get_by_id(movie_category.id) is not None

        use_case = DeleteCategory(repository)
        use_case.execute(DeleteCategoryRequest(id=movie_category.id))

        assert repository.get_by_id(movie_category.id) is None
        assert repository.get_by_id(series_category.id) is not None

    def test_when_category_not_found_raise_exception(self):
        movies_category = Category(
            name="Movie",
            description="Category for movies"
        )

        series_category = Category(
            name="Series",
            description="Category for series"
        )

        repository = InMemoryCategoryRepository([movies_category])

        use_case = DeleteCategory(repository)

        with pytest.raises(CategoryNotFound, match=f"not found category with id = {id}"):
            use_case.execute(DeleteCategoryRequest(id=series_category.id))

        assert repository.get_by_id(movies_category.id) is not None
