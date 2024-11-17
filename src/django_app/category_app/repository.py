from typing import List, Set
from django.core.paginator import Paginator

from src.core.category.domain.category import Category, CategoryId
from src.core.category.domain.category_repository import (
    CategorySearchParams,
    CategorySearchResult,
    ICategoryRepository,
)
from src.core.shared.domain.exceptions import NotFoundException
from src.core.shared.domain.repositories.search_params import SortDirection
from src.django_app.category_app.mappers import CategoryModelMapper
from src.django_app.category_app.models import CategoryModel


class CategoryDjangoRepository(ICategoryRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def insert(self, entity: Category) -> None:
        model = CategoryModelMapper.to_model(entity)
        model.save()

    def bulk_insert(self, entities: List[Category]) -> None:
        models = list(map(CategoryModelMapper.to_model, entities))
        CategoryModel.objects.bulk_create(models)

    def find_by_id(self, entity_id: CategoryId) -> Category | None:
        model = CategoryModel.objects.filter(id=entity_id).first()
        return CategoryModelMapper.to_entity(model) if model else None

    def find_by_ids(self, ids: Set[CategoryId]) -> List[Category]:
        models = CategoryModel.objects.filter(
            id__in=[str(category_id) for category_id in ids]
        )
        return [CategoryModelMapper.to_entity(model) for model in models]

    def find_by_name(self, name: str) -> Category | None:
        model = CategoryModel.objects.filter(name=name).first()
        return CategoryModelMapper.to_entity(model) if model else None

    def find_all(self) -> list[Category]:
        models = CategoryModel.objects.all()
        return [CategoryModelMapper.to_entity(model) for model in models]

    def search(self, props: CategorySearchParams) -> CategorySearchResult:
        query = CategoryModel.objects.all()

        if props.filter:
            query = query.filter(name__icontains=props.filter)

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

        return CategorySearchResult(
            items=[
                CategoryModelMapper.to_entity(model) for model in page_obj.object_list
            ],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def update(self, entity: Category) -> None:
        model = CategoryModel.objects.filter(id=entity.id.value).update(
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        if not model:
            raise NotFoundException(entity.id.value, self.get_entity())

    def delete(self, entity_id: CategoryId) -> None:
        CategoryModel.objects.filter(id=entity_id.value).delete()

    def get_entity(self) -> Category:
        return Category
