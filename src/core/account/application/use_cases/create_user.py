from dataclasses import dataclass

from src.core.account.application.use_cases.common.exceptions import UserAlreadyExistsException
from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.shared.application.cryptography import ICryptography
from src.core.shared.application.use_cases import UseCase

from src.core.account.domain.user import User
from src.core.account.domain.user_repository import IUserRepository
from src.core.account.domain.user_role import UserRole


@dataclass
class CreateUserInput:
    name: str
    email: str
    password: str
    role: UserRole | None = UserRole.USER
    is_active: bool | None = True


@dataclass
class CreateUserOutput(UserOutput):
    pass


class CreateUserUseCase(UseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        cryptography: ICryptography,
    ):
        self.user_repository = user_repository
        self.cryptography = cryptography

    def execute(self, input: CreateUserInput) -> CreateUserOutput:
        user_with_same_email = self.user_repository.find_by_email(input.email)

        if user_with_same_email:
            raise UserAlreadyExistsException()

        hashed_password = self.cryptography.hash(input.password)

        user = User(
            name=input.name,
            email=input.email,
            password=hashed_password,
            role=input.role, 
            is_active=input.is_active,
        )

        self.user_repository.insert(user)

        return self.__to_output(user)

    def __to_output(self, user: User):
        return CreateUserOutput.from_entity(user)
