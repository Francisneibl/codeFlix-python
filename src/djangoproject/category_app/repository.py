from uuid import UUID

from src.core.category.domain.Category import Category
from src.core.category.domain.category_repository import CategoryRepository
from djangoproject.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model

    def save(self, category: Category):
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id)
            return Category(
                name=category.name,
                description=category.description,
                id=category.id,
                is_active=category.is_active
            )
        except self.category_model.DoesNotExist:
            return None

    def list(self) -> list[Category]:
        categories = self.category_model.objects.all()

        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ]

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
