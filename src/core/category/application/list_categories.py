from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoriesRequest:
    pass


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str | None
    is_active: bool


@dataclass
class ListCategoriesResponse:
    data: list[CategoryOutput]


class ListCategories:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self):
        categories = self.repository.list()

        return ListCategoriesResponse(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active
                ) for category in categories]
        )
