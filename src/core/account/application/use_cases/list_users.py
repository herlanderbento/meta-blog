from dataclasses import dataclass

from src.core.shared.application.pagination_output import PaginationOutput
from src.core.shared.application.search_input import SearchInput
from src.core.shared.application.use_cases import UseCase
from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.account.domain.user_repository import (
    IUserRepository,
    UserFilter,
    UserSearchParams,
    UserSearchResult,
)


@dataclass(slots=True)
class ListUsersInput(SearchInput[UserFilter]):
    pass


@dataclass(slots=True)
class ListUsersOutput(PaginationOutput[UserOutput]):
    pass


class ListUsersUseCase(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, input: ListUsersInput) -> ListUsersOutput:
        params = UserSearchParams(**input.to_input())

        result = self.user_repository.search(params)

        return self.__to_output(result)

    def __to_output(self, result: UserSearchResult) -> ListUsersOutput:
        item = list(map(UserOutput.from_entity, result.items))
        return ListUsersOutput.from_search_result(item, result)
