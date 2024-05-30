from src.core.category.application.category_repository import CategoryRepository
from uuid import UUID
from dataclasses import dataclass

from src.core.category.application.exceptions import CategoryNotFound


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryRequest):
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"not found category with id = {id}")

        self.repository.delete(request.id)
