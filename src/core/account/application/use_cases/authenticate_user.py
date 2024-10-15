from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


from src.core.shared.application.cryptography import ICryptography
from src.core.shared.application.token_generator import ITokenGenerator
from src.core.shared.application.use_cases import UseCase
from src.core.account.application.use_cases.common.exceptions import (
    InvalidCredentialsException,
)
from src.core.account.domain.user import User
from src.core.account.domain.user_repository import IUserRepository
from src.core.account.domain.user_token import UserToken
from src.core.account.domain.user_token_repository import IUserTokenRepository


@dataclass
class AuthenticateUserInput:
    email: str
    password: str


@dataclass
class UserOutput:
    id: str
    name: str
    email: str
    is_staff: bool
    is_superuser: bool


@dataclass
class AuthenticateUserOutput:
    user: UserOutput
    token: str
    token_type: str = "Bearer"
    expires_in: int = 3600


class AuthenticateUserUseCase(UseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        user_token_repository: IUserTokenRepository,
        cryptography: ICryptography,
        token_generator: ITokenGenerator,
    ):
        self.user_repository = user_repository
        self.user_token_repository = user_token_repository
        self.cryptography = cryptography
        self.token_generator = token_generator

    def execute(self, input: AuthenticateUserInput) -> AuthenticateUserOutput:
        user = self.user_repository.find_by_email(input.email)

        if user is None:
            raise InvalidCredentialsException()

        if not self.cryptography.verify(input.password, user.password):
            raise InvalidCredentialsException()

        token = self.__generate_token(user)

        user_token = UserToken.create(
            user_id=user.id,
            refresh_token=token,
        )

        self.user_token_repository.insert(user_token)

        return AuthenticateUserOutput(
            token=token,
            user=UserOutput(
                id=user.id,
                name=user.name,
                email=user.email,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
            ),
        )

    def __generate_token(self, user: User) -> str:
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3600),
        }
        return self.token_generator.generate(payload)
