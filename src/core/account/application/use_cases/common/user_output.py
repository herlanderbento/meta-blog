from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.account.domain.user import User
from src.core.account.domain.user_role import UserRole


@dataclass(slots=True)
class UserOutput:
    id: UUID
    name: str
    email: str
    role: UserRole | None
    is_active: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: User):
        return cls(
            id=entity.id.value,
            name=entity.name,
            email=entity.email,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
