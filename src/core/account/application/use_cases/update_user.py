from dataclasses import dataclass
from uuid import UUID

from src.core.shared.application.cryptography import ICryptography
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.account.application.use_cases.common.exceptions import (
    UserAlreadyExistsException,
)
from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.account.domain.user import User
from src.core.account.domain.user_repository import IUserRepository


@dataclass
class UpdateUserInput:
    id: UUID
    name: str | None = None
    email: str | None = None
    password: str | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None


@dataclass
class UpdateUserOutput(UserOutput):
    pass


class UpdateUserUseCase(UseCase):
    def __init__(
        self,
        user_repo: IUserRepository,
        cryptography: ICryptography,
    ):
        self.user_repo = user_repo
        self.cryptography = cryptography

    def execute(self, input: UpdateUserInput) -> UpdateUserOutput:
        user = self.user_repo.find_by_id(input.id)

        if user is None:
            raise NotFoundException(input.id, User)

        if input.name is not None:
            user.change_name(input.name)

        if input.email != None and input.email != user.email:
            user_with_same_email = self.user_repo.find_by_email(input.email)

            if user_with_same_email:
                raise UserAlreadyExistsException()

            user.change_email(input.email)

        if input.password is not None:
            hashed_password = self.cryptography.hash(input.password)
            user.change_password(hashed_password)

        if input.is_staff is not None:
            user.change_is_staff(input.is_staff)

        if input.is_superuser is not None:
            user.change_is_superuser(input.is_superuser)

        if input.is_active is True:
            user.activate()

        if input.is_active is False:
            user.deactivate()

        if user.notification.has_errors():
            raise EntityValidationException(user.notification.errors)

        self.user_repo.update(user)

        return self.__to_output(user)

    def __to_output(self, user: User):
        return UpdateUserOutput.from_entity(user)
