from dataclasses import dataclass

from src.core.category.application.use_cases.common.category_output import CategoryOutput
from src.core.category.domain.category_repository import (
    CategorySearchParams,
    CategorySearchResult,
    ICategoryRepository,
)
from src.core.shared.application.pagination_output import PaginationOutput
from src.core.shared.application.search_input import SearchInput
from src.core.shared.application.use_cases import UseCase


@dataclass(slots=True)
class ListCategoriesInput(SearchInput[str]):
    pass


@dataclass(slots=True)
class ListCategoriesOutput(PaginationOutput[CategoryOutput]):
    pass


class ListCategoriesUseCase(UseCase):

    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def execute(self, input: ListCategoriesInput) -> ListCategoriesOutput:
        params = CategorySearchParams(**input.to_input())

        result = self.category_repo.search(params)

        return self.__to_output(result)

    def __to_output(self, result: CategorySearchResult) -> ListCategoriesOutput:
        items = list(map(CategoryOutput.from_entity, result.items))
        return ListCategoriesOutput.from_search_result(items, result)
