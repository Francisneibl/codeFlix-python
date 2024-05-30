import pytest

from src.core.category.domain.Category import Category
from djangoproject.category_app.repository import DjangoORMCategoryRepository
from djangoproject.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Movies",
            description="Category for movies"
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get(id=category.id)
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active
