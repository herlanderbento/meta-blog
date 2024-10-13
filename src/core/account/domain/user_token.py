from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Annotated
from src.core.shared.domain.entity import AggregateRoot
from src.core.shared.domain.value_objects import Uuid
from src.core.account.domain.user import UserId


class UserTokenId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class UserToken(AggregateRoot):
    id: UserTokenId = field(default_factory=UserTokenId)
    user_id: UserId
    refresh_token: str
    expires_date: datetime
    created_at: Annotated[datetime, datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def create(
        user_id: UserId,
        refresh_token: str,
    ) -> "UserToken":
        return UserToken(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_date=datetime.now(timezone.utc) + timedelta(seconds=3600),
        )

    @property
    def entity_id(self):
        return self.id

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "user_id": self.user_id,
                "refresh_token": self.refresh_token,
                "expires_date": self.expires_date,
                "created_at": self.created_at,
            }
        )
