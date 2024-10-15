from dataclasses import dataclass

from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.account.domain.user import User, UserId
from src.core.account.domain.user_repository import IUserRepository
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import NotFoundException


@dataclass
class GetUserInput:
    user_id: UserId


@dataclass
class GetUserOutput(UserOutput):
    pass


class GetUserUseCase(UseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
    ):
        self.user_repository = user_repository

    def execute(self, input: GetUserInput) -> GetUserOutput:
        if user := self.user_repository.find_by_id(input.user_id):
            return self.__to_output(user)
        else:
            raise NotFoundException(input.user_id, User)

    def __to_output(self, entity: User) -> GetUserOutput:
        return GetUserOutput.from_entity(entity)
