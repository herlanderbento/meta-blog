from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes
from django.utils.decorators import method_decorator

from src.core.shared.infra.cryptography.bcrypt_hasher import BcryptHasher
from src.core.account.application.use_cases.common.user_output import UserOutput
from src.core.account.application.use_cases.create_user import (
    CreateUserInput,
    CreateUserUseCase,
)
from src.core.account.application.use_cases.list_users import (
    ListUsersInput,
    ListUsersUseCase,
)
from src.core.account.domain.user_repository import UserFilter
from src.django_app.account_app.models import UserModel
from src.django_app.account_app.presenters import UserCollectionPresenter, UserPresenter
from src.django_app.account_app.repository import UserDjangoRepository
from src.django_app.account_app.serializers import CreateUserInputSerializer
from src.django_app.permissions import IsAdmin, IsAuthenticated
from src.django_app.shared_app.filter_extractor import FilterExtractor


class UserViewSet(viewsets.ViewSet, FilterExtractor):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def __init__(self, **kwargs) -> None:
        user_repo = UserDjangoRepository()
        cryptography = BcryptHasher()

        self.create_use_case = CreateUserUseCase(user_repo, cryptography)
        self.list_use_case = ListUsersUseCase(user_repo)

    def create(self, request: Request) -> Response:
        serializer = CreateUserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _input = CreateUserInput(**serializer.validated_data)

        output = self.create_use_case.execute(_input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=UserViewSet.serialize(output),
        )

    def list(self, request: Request) -> Response:
        query_params = request.query_params.dict()

        filters = self.extract_filters(query_params, ["name", "email", "role"])

        _input = ListUsersInput(**query_params, filter=UserFilter(**filters))

        output = self.list_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=UserCollectionPresenter(output).serialize(),
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        raise NotImplementedError()

    def partial_update(self, request, pk: UUID = None):
        raise NotImplementedError()

    def destroy(self, request: Request, pk: UUID = None):
        raise NotImplementedError()

    @staticmethod
    def serialize(output: UserOutput):
        return UserPresenter.from_output(output).serialize()
    
    def get_queryset(self):
        return UserModel.objects.all()
