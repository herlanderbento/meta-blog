from uuid import UUID
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.core.account.application.use_cases.delete_user import (
    DeleteUserInput,
    DeleteUserUseCase,
)
from src.core.account.application.use_cases.get_user import GetUserInput, GetUserUseCase
from src.core.account.application.use_cases.update_user import (
    UpdateUserInput,
    UpdateUserUseCase,
)
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
from src.django_app.account_app.documentations import UserDocumentation
from src.django_app.account_app.presenters import UserCollectionPresenter, UserPresenter
from src.django_app.account_app.repository import UserDjangoRepository
from src.django_app.account_app.serializers import (
    ChangeUserPermissionInputSerializer,
    CreateUserInputSerializer,
    DeleteUserInputSerializer,
    GetUserInputSerializer,
    UpdateUserInputSerializer,
)
from src.django_app.shared_app.filter_extractor import FilterExtractor


class UserAPIView(APIView, FilterExtractor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        user_repo = UserDjangoRepository()
        cryptography = BcryptHasher()

        self.create_use_case = CreateUserUseCase(user_repo, cryptography)
        self.get_use_case = GetUserUseCase(user_repo)
        self.list_use_case = ListUsersUseCase(user_repo)
        self.update_use_case = UpdateUserUseCase(user_repo, cryptography)
        self.delete_use_case = DeleteUserUseCase(user_repo)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=CreateUserInputSerializer,
        responses={
            201: openapi.Response(
                "User created successfully",
                schema=UserDocumentation.user_response_schema(),
            ),
            422: "Invalid data",
        },
    )
    def post(self, request: Request) -> Response:
        serializer = CreateUserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _input = CreateUserInput(**serializer.validated_data)

        output = self.create_use_case.execute(_input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.serialize(output),
        )

    @swagger_auto_schema(
        operation_description="List users",
        manual_parameters=UserDocumentation.user_query_parameters(),
        responses={
            200: openapi.Response(
                "User found successfully",
                schema=UserDocumentation.user_list_response_schema(),
            ),
        },
    )
    def get(self, request: Request, user_id: UUID = None) -> Response:
        if user_id is not None:
            return self.get_object(user_id)

        query_params = request.query_params.dict()

        filters = self.extract_filters(
            query_params, ["name", "email", "is_staff", "is_superuser", "is_active"]
        )
        _input = ListUsersInput(**query_params, filter=UserFilter(**filters))

        output = self.list_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=UserCollectionPresenter(output).serialize(),
        )

    @swagger_auto_schema(
        operation_description="Get a new user",
        request_body=GetUserInputSerializer,
        responses={
            200: openapi.Response(
                "Get user successfully",
                schema=UserDocumentation.user_response_schema(),
            ),
            404: "User not found",
        },
    )
    def get_object(self, user_id: UUID) -> Response:
        serializer = GetUserInputSerializer(data={"user_id": user_id})
        serializer.is_valid(raise_exception=True)

        _input = GetUserInput(**serializer.validated_data)

        output = self.get_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=self.serialize(output),
        )

    @swagger_auto_schema(
        operation_description="Update a new user",
        request_body=UpdateUserInputSerializer,
        responses={
            201: openapi.Response(
                "User updated successfully",
                schema=UserDocumentation.user_response_schema(),
            ),
            422: "Invalid data",
        },
    )
    def patch(self, request: Request, user_id: UUID) -> Response:
        if request.path.endswith("change-permission"):
            return self.patch_change_permission(request, user_id)

        serializer = UpdateUserInputSerializer(
            data={**request.data, "id": user_id},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        _input = UpdateUserInput(**serializer.validated_data)

        output = self.update_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=self.serialize(output),
        )

    @swagger_auto_schema(
        operation_description="Change permission a new user",
        request_body=ChangeUserPermissionInputSerializer,
        responses={
            204: openapi.Response("User updated successfully"),
            422: "Invalid data",
        },
    )
    def patch_change_permission(self, request: Request, user_id: UUID) -> Response:
        serializer = ChangeUserPermissionInputSerializer(
            data={**request.data, "id": user_id},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        _input = UpdateUserInput(**serializer.validated_data)

        self.update_use_case.execute(_input)

        return Response(status=status.HTTP_204_NO_CONTENT)


    @swagger_auto_schema(
        operation_description="Delete a new user",
        request_body=DeleteUserInputSerializer,
        responses={
            204: openapi.Response("User deleted successfully"),
            404: "User not found",
        },
    )
    def delete(self, request: Request, user_id: UUID) -> Response:
        serializer = DeleteUserInputSerializer(data={"id": user_id})
        serializer.is_valid(raise_exception=True)

        _input = DeleteUserInput(**serializer.validated_data)

        self.delete_use_case.execute(_input)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "PATCH" and self.request.path.endswith(
            "change-permission"
        ):
            return [IsAuthenticated(), IsAdminUser()]

        # if self.request.method == "GET" and self.kwargs.get("user_id"):
        #     return [IsAuthenticated()]

        permissions_map = {
            "GET": [],
            "POST": [AllowAny()],
            "PUT": [IsAuthenticated()],
            "PATCH": [IsAuthenticated()],
            "DELETE": [IsAuthenticated(), IsAdminUser()],
        }

        return permissions_map.get(self.request.method, super().get_permissions())

    @staticmethod
    def serialize(output: UserOutput):
        return UserPresenter.from_output(output).serialize()
