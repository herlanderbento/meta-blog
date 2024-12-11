from dataclasses import dataclass, field
import datetime
from typing import Annotated

from pydantic import Strict, StrictBool
from src.core.shared.domain.entity import AggregateRoot
from src.core.shared.domain.value_objects import Uuid


@dataclass
class CategoryCreateCommand:
    name: str
    description: str | None = None
    is_active: StrictBool = True


class CategoryId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class Category(AggregateRoot):
    id: CategoryId = field(default_factory=CategoryId)
    name: str
    description: str | None = None
    is_active: StrictBool = True
    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(command: CategoryCreateCommand):
        return Category(
            name=command.name,
            description=command.description,
            is_active=command.is_active,
        )

    @property
    def entity_id(self) -> Uuid:
        return self.id.value

    def change_name(self, name: str):
        self.name = name
        self.touch()
        self.validate()


    def change_description(self, description: str | None):
        self.description = description
        self.touch()
        self.validate()


    def activate(self):
        self.is_active = True
        self.touch()


    def deactivate(self):
        self.is_active = False
        self.touch()


    def touch(self):
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "is_active": self.is_active,
                "created_at": self.created_at,
                "updated_at": self.created_at,
            }
        )
