from rest_framework import permissions
from rest_framework.views import APIView

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from src.core.account.application.use_cases.authenticate_user import (
    AuthenticateUserInput,
    AuthenticateUserUseCase,
)
from src.core.shared.infra.cryptography.bcrypt_hasher import BcryptHasher
from src.django_app.account_app.repository import UserDjangoRepository
from src.django_app.authentication_app.repository import UserTokenDjangoRepository
from src.django_app.authentication_app.serializers import (
    AuthenticateUserInputSerializer,
)
from src.django_app.authentication_app.services.jwt_auth_service import JwtAuthService


class AuthenticationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs) -> None:
        user_repo = UserDjangoRepository()
        user_token_repo = UserTokenDjangoRepository()
        cryptography = BcryptHasher()
        jwt_token_generator = JwtAuthService()

        self.authenticate_user = AuthenticateUserUseCase(
            user_repo,
            user_token_repo,
            cryptography,
            jwt_token_generator,
        )

    def post(self, request: Request) -> Response:
        serializer = AuthenticateUserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _input = AuthenticateUserInput(**serializer.validated_data)

        output = self.authenticate_user.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "token": output.token,
                "token_type": output.token_type,
                "expires_in": output.expires_in,
                "user": {
                    "id": output.user.id.value,
                    "email": output.user.email,
                    "name": output.user.name,
                    "is_staff": output.user.is_staff,
                    "is_superuser": output.user.is_superuser,
                },
            },
        )
