from typing import List, Set
from django.core.paginator import Paginator

from src.core.shared.domain.exceptions import (
    NotFoundException,
)
from src.core.shared.domain.repositories.search_params import SortDirection
from src.core.account.domain.user import User, UserId
from src.core.account.domain.user_repository import (
    IUserRepository,
    UserSearchParams,
    UserSearchResult,
)
from src.django_app.account_app.mappers import UserModelMapper
from src.django_app.account_app.models import UserModel


class UserDjangoRepository(IUserRepository):
    sortable_fields = ["name", "created_at"]

    def insert(self, entity: User) -> None:
        model = UserModelMapper.to_model(entity)
        model.save()

    def bulk_insert(self, entities: List[User]) -> None:
        models = list(map(UserModelMapper.to_model, entities))
        UserModel.objects.bulk_create(models)

    def find_by_id(self, entity_id: UserId) -> User | None:
        model = UserModel.objects.filter(id=entity_id).first()
        return UserModelMapper.to_entity(model) if model else None

    def find_by_ids(self, entity_ids: Set[UserId]) -> List[User]:
        models = UserModel.objects.filter(
            id__in=[str(entity_id.value) for entity_id in entity_ids]
        )
        return [UserModelMapper.to_entity(model) for model in models]

    def find_by_email(self, email: str) -> User | None:
        model = UserModel.objects.filter(email=email).first()
        return UserModelMapper.to_entity(model) if model else None

    def find_all(self) -> List[User]:
        models = UserModel.objects.all()
        return [UserModelMapper.to_entity(model) for model in models]

    def update(self, entity: User) -> None:
        model = UserModel.objects.filter(id=entity.id.value).update(
            name=entity.name,
            email=entity.email,
            password=entity.password,
            is_staff=entity.is_staff,
            is_superuser=entity.is_superuser,
            is_active=entity.is_active,
            updated_at=entity.updated_at,
        )

        if not model:
            raise NotFoundException(entity.id.value, self.get_entity())

    def search(self, props: UserSearchParams) -> UserSearchResult:
        query = UserModel.objects.all()

        if props.filter:
            if props.filter.name:
                query = query.filter(name__icontains=props.filter.name)

            if props.filter.email:
                query = query.filter(email__icontains=props.filter.email)

            if props.filter.is_staff:
                query = query.filter(is_staff=props.filter.is_staff)

            if props.filter.is_superuser:
                query = query.filter(is_superuser=props.filter.is_superuser)

            if props.filter.is_active:
                query = query.filter(is_active=props.filter.is_active)

        if props.sort and props.sort in self.sortable_fields:
            if props.sort_dir == SortDirection.DESC:
                props.sort = f"-{props.sort}"
            query = query.order_by(props.sort)
        else:
            query = query.order_by("-created_at")

        paginator = Paginator(query, props.per_page)

        if props.page <= paginator.num_pages:
            page_obj = paginator.page(props.page)
        else:
            page_obj = paginator.page(paginator.num_pages)
            page_obj.object_list = []

        return UserSearchResult(
            items=[UserModelMapper.to_entity(model) for model in page_obj.object_list],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def delete(self, entity_id: UserId) -> None:
        UserModel.objects.filter(id=entity_id).delete()

    def get_entity(self) -> User:
        return User
