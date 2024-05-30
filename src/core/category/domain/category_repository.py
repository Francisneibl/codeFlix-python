from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.Category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    def get_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, category: Category):
        raise NotImplementedError

    def list(self) -> list[Category]:
        raise NotImplementedError
