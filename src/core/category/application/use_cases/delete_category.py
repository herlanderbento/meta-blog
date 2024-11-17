from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import NotFoundException


@dataclass
class DeleteCategoryInput:
    category_id: UUID


class DeleteCategoryUseCase(UseCase):
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def execute(self, input: DeleteCategoryInput) -> None:
        category = self.category_repo.find_by_id(input.category_id)


        if category is None:
            raise NotFoundException(input.category_id, Category)

        self.category_repo.delete(category.id)
