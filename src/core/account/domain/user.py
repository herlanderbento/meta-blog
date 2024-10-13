from dataclasses import dataclass, field
import datetime
from typing import Annotated

from pydantic import Strict
from src.core.shared.domain.entity import AggregateRoot
from src.core.shared.domain.value_objects import Uuid
from src.core.account.domain.user_role import UserRole


@dataclass
class CreateUserCommand:
    name: str
    email: str
    password: str
    role: UserRole | None = UserRole.USER
    is_active: bool | None = True


class UserId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class User(AggregateRoot):
    id: UserId = field(default_factory=UserId)
    name: str
    email: str
    password: str
    role: UserRole | None = UserRole.USER
    is_active: bool | None = True
    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(props: CreateUserCommand) -> "User":
        return User(
            name=props.name,
            email=props.email,
            password=props.password,
            role=props.role,
            is_active=props.is_active,
        )

    @property
    def entity_id(self):
        return self.id.value

    def change_name(self, name: str):
        self.name = name
        self.touch()
        self.validate()

    def change_email(self, email: str):
        self.email = email
        self.touch()
        self.validate()

    def change_password(self, password: str):
        self.password = password
        self.touch()
        self.validate()

    def change_role(self, role: UserRole):
        self.role = role
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
                "email": self.email,
                "password": self.password,
                "role": self.role,
                "is_active": self.is_active,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }
        )
