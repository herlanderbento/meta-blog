from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import NotFoundException


@dataclass
class GetCategoryInput:
    category_id: UUID


@dataclass
class GetCategoryOutput(CategoryOutput):
    pass


class GetCategoryUseCase(UseCase):

    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def execute(self, input: GetCategoryInput) -> GetCategoryOutput:
        if category := self.category_repo.find_by_id(input.category_id):
            return self.__to_output(category)
        else:
            raise NotFoundException(input.category_id, Category)

    def __to_output(self, entity: Category):
        return GetCategoryOutput.from_entity(entity)
