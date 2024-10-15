from typing import List, Type
from src.core.shared.domain.repositories.search_params import SortDirection
from src.core.shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core.account.domain.user import User, UserId
from src.core.account.domain.user_repository import IUserRepository, UserFilter


class UserInMemoryRepository(
    IUserRepository, InMemorySearchableRepository[User, UserId, UserFilter]
):
    sortable_fields: List[str] = ["name", "created_at"]

    def find_by_email(self, email: str) -> User | None:
        return next((user for user in self.items if user.email == email), None)

    def _apply_filter(
        self, items: List[User], filter_param: UserFilter | None
    ) -> List[User]:
        if filter_param:
            filter_obj = filter(
                lambda item: self._filter_logic(item, filter_param), items
            )
            return list(filter_obj)

        return items

    def _filter_logic(self, item: User, filter_param: UserFilter) -> bool:
        if filter_param.name and filter_param.email and filter_param.role:
            return self._clause_name(item, filter_param.name) and self._clause_email(
                item, filter_param.email
            )

        return (
            self._clause_name(item, filter_param.name)
            if filter_param.name
            else (self._clause_email(item, filter_param.email))
        )

    def _clause_name(self, item: User, name: str) -> bool:
        return name.lower() in item.name.lower()

    def _clause_email(self, item: User, email: str) -> bool:
        return email.lower() in item.email.lower()

    def _apply_sort(
        self,
        items: List[User],
        sort: str | None = None,
        sort_dir: SortDirection | None = None,
    ) -> List[User]:
        return (
            super()._apply_sort(items, sort, sort_dir)
            if sort
            else super()._apply_sort(items, "created_at", SortDirection.DESC)
        )

    def get_entity(self) -> Type[User]:
        return User
