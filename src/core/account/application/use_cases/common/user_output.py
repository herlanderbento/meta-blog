from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.account.domain.user import User


@dataclass(slots=True)
class UserOutput:
    id: UUID
    name: str
    email: str
    is_staff: bool | None
    is_superuser: bool | None
    is_active: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: User):
        return cls(
            id=entity.id.value,
            name=entity.name,
            email=entity.email,
            is_staff=entity.is_staff,
            is_superuser=entity.is_superuser,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
