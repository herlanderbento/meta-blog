from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.common.category_output import CategoryOutput
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import EntityValidationException, NotFoundException


@dataclass
class UpdateCategoryInput:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategoryOutput(CategoryOutput):
    pass


class UpdateCategoryUseCase(UseCase):
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def execute(self, input: UpdateCategoryInput) -> UpdateCategoryOutput:
        category = self.category_repo.find_by_id(input.id)

        if category is None:
            raise NotFoundException(input.id, Category)

        if input.name is not None:
            category.change_name(input.name)

        if input.description is not None:
            category.change_description(input.description)

        if input.is_active is True:
            category.activate()

        if input.is_active is False:
            category.deactivate()

        if category.notification.has_errors():
            raise EntityValidationException(category.notification.errors)

        self.category_repo.update(category)

        return self.__to_output(category)

    def __to_output(self, entity: Category):
        return UpdateCategoryOutput.from_entity(entity)
