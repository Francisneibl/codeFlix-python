from dataclasses import dataclass, field
from typing import Set
from uuid import uuid4, UUID


@dataclass
class Genre:
    name: str
    categories: Set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True

    def __eq__(self, other):
        if isinstance(other, Genre):
            return False

        return self.id == other.id

    def change_name(self, name: str):
        pass

    def add_category(self, category_id: UUID):
        pass

    def remove_category(self, category_id: UUID):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass
