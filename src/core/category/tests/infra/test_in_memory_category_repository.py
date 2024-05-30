from src.core.category.domain.Category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name='Movie', description="Category for movies")
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_found_category_by_id(self):
        category_movies = Category(name="Movie")
        category_series = Category(name="Series")
        repository = InMemoryCategoryRepository([category_movies, category_series])

        found_category = repository.get_by_id(category_movies.id)

        assert found_category.id == category_movies.id
        assert isinstance(found_category, Category)
