from src.core.category.application.list_categories import ListCategories, ListCategoriesResponse, CategoryOutput
from src.core.category.domain.Category import Category

from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategories:
    def test_list_category_when_repository_is_empty(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategories(repository)
        categories = use_case.execute()

        assert categories == ListCategoriesResponse(data=[])

    def test_list_all_categories(self):
        movie_category = Category(
            name="Movies",
            description="Category for movies"
        )

        series_category = Category(
            name="Series",
            description="Series for movies"
        )

        repository = InMemoryCategoryRepository([movie_category, series_category])

        use_case = ListCategories(repository)
        categories = use_case.execute()

        assert categories == ListCategoriesResponse(data=[
            CategoryOutput(
                name=movie_category.name,
                description=movie_category.description,
                id=movie_category.id,
                is_active=movie_category.is_active
            ),
            CategoryOutput(
                name=series_category.name,
                description=series_category.description,
                id=series_category.id,
                is_active=series_category.is_active
            )
        ])
