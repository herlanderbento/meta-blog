from abc import ABC
from dataclasses import dataclass, field

from src.core.shared.domain.repositories.repository_interface import (
    ISearchableRepository,
)
from src.core.shared.domain.repositories.search_params import SearchParams
from src.core.shared.domain.repositories.search_result import SearchResult
from src.core.account.domain.user import User, UserId
from src.core.account.domain.user_role import UserRole


@dataclass(frozen=True, slots=True)
class UserFilter:
    name: str | None = field(default=None)
    email: str | None = field(default=None)
    role: UserRole | None = field(default=None)


class UserSearchParams(SearchParams[UserFilter]):
    pass


class UserSearchResult(SearchResult[User]):
    pass


class IUserRepository(ISearchableRepository[User, UserId], ABC):
    def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError()
