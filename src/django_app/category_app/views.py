from uuid import UUID
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategoryInput,
    CreateCategoryUseCase,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategoryInput,
    DeleteCategoryUseCase,
)
from src.core.category.application.use_cases.get_category import (
    GetCategoryInput,
    GetCategoryUseCase,
)
from src.core.category.application.use_cases.list_categories import (
    ListCategoriesInput,
    ListCategoriesUseCase,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategoryInput,
    UpdateCategoryUseCase,
)
from src.django_app.category_app.presenters import (
    CategoryCollectionPresenter,
    CategoryPresenter,
)
from src.django_app.category_app.repository import CategoryDjangoRepository
from src.django_app.category_app.serializers import (
    CreateCategoryInputSerializer,
    DeleteCategoryInputSerializer,
    GetCategoryInputSerializer,
    UpdateCategoryInputSerializer,
)
from src.django_app.shared_app.filter_extractor import FilterExtractor


class CategoryAPIView(APIView, FilterExtractor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        repository = CategoryDjangoRepository()

        self.create_use_case = CreateCategoryUseCase(repository)
        self.list_use_case = ListCategoriesUseCase(repository)
        self.get_use_case = GetCategoryUseCase(repository)
        self.update_use_case = UpdateCategoryUseCase(repository)
        self.delete_use_case = DeleteCategoryUseCase(repository)

    def post(self, request: Request) -> Response:
        serializer = CreateCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _input = CreateCategoryInput(**serializer.validated_data)

        output = self.create_use_case.execute(_input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.serialize(output),
        )

    def get(self, request: Request, category_id: UUID = None) -> Response:
        if category_id is not None:
            return self.get_object(category_id)

        query_params = request.query_params.dict()

        _input = ListCategoriesInput(**query_params)

        output = self.list_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=CategoryCollectionPresenter(output).serialize(),
        )

    def get_object(self, category_id: UUID) -> Response:
        serializer = GetCategoryInputSerializer(data={"category_id": category_id})
        serializer.is_valid(raise_exception=True)

        _input = GetCategoryInput(**serializer.validated_data)

        output = self.get_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=self.serialize(output),
        )

    def patch(self, request: Request, category_id: UUID) -> Response:
        serializer = UpdateCategoryInputSerializer(
            data={**request.data, "id": category_id},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        _input = UpdateCategoryInput(**serializer.validated_data)

        output = self.update_use_case.execute(_input)

        return Response(
            status=status.HTTP_200_OK,
            data=self.serialize(output),
        )

    def delete(self, request: Request, category_id: UUID) -> Response:
        serializer = DeleteCategoryInputSerializer(data={"category_id": category_id})
        serializer.is_valid(raise_exception=True)

        _input = DeleteCategoryInput(**serializer.validated_data)

        self.delete_use_case.execute(_input)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        permissions_map = {
            "GET": [AllowAny()],
            "POST": [IsAuthenticated(), IsAdminUser()],
            "PUT": [IsAuthenticated(), IsAdminUser()],
            "PATCH": [IsAuthenticated(), IsAdminUser()],
            "DELETE": [IsAuthenticated(), IsAdminUser()],
        }

        return permissions_map.get(self.request.method, super().get_permissions())

    @staticmethod
    def serialize(output: CategoryOutput):
        return CategoryPresenter.from_output(output).serialize()
