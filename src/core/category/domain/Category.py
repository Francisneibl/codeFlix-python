from dataclasses import dataclass, field
from uuid import uuid4, UUID


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False

        return self.id == other.id

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must not have longer than 255 characters")
        elif len(self.name) <= 0:
            raise ValueError("name cannot be empty")

    def update_category(self, name, description):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()
