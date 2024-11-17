from dataclasses import dataclass

from src.core.category.application.use_cases.common.exceptions import CategoryAlreadyExistsException
from src.core.shared.domain.exceptions import EntityValidationException
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.shared.application.use_cases import UseCase
from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)


@dataclass
class CreateCategoryInput:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryOutput(CategoryOutput):
    pass


class CreateCategoryUseCase(UseCase):
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def execute(self, input: CreateCategoryInput) -> CreateCategoryOutput:
        category_with_same_name = self.category_repo.find_by_name(input.name)

        if category_with_same_name:
            raise CategoryAlreadyExistsException()

        category = Category.create(input)

        if category.notification.has_errors():
            raise EntityValidationException(category.notification.errors)

        self.category_repo.insert(category)

        return self.__to_output(category)

    def __to_output(self, entity: Category):
        return CreateCategoryOutput.from_entity(entity)
