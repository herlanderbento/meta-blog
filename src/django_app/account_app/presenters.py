from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.account.application.use_cases.list_users import ListUsersOutput
from src.core.account.domain.user_role import UserRole
from src.django_app.shared_app.presenters import CollectionPresenter, ResourcePresenter


@dataclass(slots=True)
class UserPresenter(ResourcePresenter):
    id: UUID
    name: str
    email: str
    is_staff: bool | None
    is_superuser: bool | None
    is_active: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_output(cls, output: UserOutput):
        return cls(
            id=output.id,
            name=output.name,
            email=output.email,
            is_staff=output.is_staff,
            is_superuser=output.is_superuser,
            is_active=output.is_active,
            created_at=output.created_at,
            updated_at=output.updated_at,
        )


@dataclass(slots=True)
class UserCollectionPresenter(CollectionPresenter):
    output: ListUsersOutput

    def __post_init__(self):
        self.data = [UserPresenter.from_output(item) for item in self.output.items]

        self.pagination = self.output
