from abc import ABC

from src.core.account.domain.user_token import UserToken, UserTokenId


class IUserTokenRepository(ABC):
    def insert(self, entity: UserToken) -> None:
        raise NotImplementedError()

    def find_by_refresh_token(self, refresh_token: str) -> UserToken | None:
        raise NotImplementedError()

    def delete(self, entity_id: UserTokenId) -> None:
        raise NotImplementedError()
