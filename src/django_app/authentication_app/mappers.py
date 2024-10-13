from dataclasses import dataclass
from typing import Tuple

from src.core.account.domain.user import UserId
from src.core.account.domain.user_token import UserToken, UserTokenId
from src.django_app.authentication_app.models import UserTokenModel


@dataclass
class UserTokenRelations:
    user_id: str


class UserTokenModelMapper:

    @staticmethod
    def to_model(entity: UserToken) -> Tuple["UserTokenModel", UserTokenRelations]:
        return UserTokenModel(
            id=entity.id.value,
            refresh_token=entity.refresh_token,
            expires_date=entity.expires_date,
            created_at=entity.created_at,
        ), UserTokenRelations(user_id=entity.user_id.value)

    @staticmethod
    def to_entity(model: UserTokenModel) -> UserToken:
        return UserToken(
            id=UserTokenId(model.id),
            user_id=UserId(model.user.id),
            refresh_token=model.refresh_token,
            expires_date=model.expires_date,
            created_at=model.created_at,
        )
