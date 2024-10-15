from dataclasses import dataclass
from uuid import UUID

from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import NotFoundException
from src.core.account.domain.user import User
from src.core.account.domain.user_repository import IUserRepository


@dataclass
class DeleteUserInput:
    user_id: UUID


class DeleteUserUseCase(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, input: DeleteUserInput) -> None:
        if user := self.user_repository.find_by_id(input.user_id):
            self.user_repository.delete(user.id.value)
        else:
            raise NotFoundException(input.user_id, User)
