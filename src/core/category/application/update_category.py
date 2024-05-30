from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str = None
    description: str = None
    is_activate: bool = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest):
        category = self.repository.get_by_id(request.id)

        if not category:
            raise CategoryNotFound(f"not found category with id = {request.id}")

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name

        if request.description is not None:
            current_description = request.description

        category.update_category(name=current_name, description=current_description)

        if request.is_activate is True:
            category.activate()

        if request.is_activate is False:
            category.deactivate()

        self.repository.update(category)
