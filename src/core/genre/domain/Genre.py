from dataclasses import dataclass, field
from typing import Set
from uuid import uuid4, UUID


@dataclass
class Genre:
    name: str
    categories: Set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False

        return self.id == other.id

    def validate(self):
        if not self.name:
            raise ValueError('name cannot be empty')

        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255 characters')

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
