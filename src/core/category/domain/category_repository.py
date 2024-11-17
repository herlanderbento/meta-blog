from abc import ABC
from src.core.category.domain.category import Category, CategoryId
from src.core.shared.domain.repositories.repository_interface import ISearchableRepository
from src.core.shared.domain.repositories.search_params import SearchParams
from src.core.shared.domain.repositories.search_result import SearchResult


class CategorySearchParams(SearchParams[str]):
    pass


class CategorySearchResult(SearchResult[Category]):
    pass


class ICategoryRepository(ISearchableRepository[Category, CategoryId], ABC):
     def find_by_name(self, name: str) -> Category | None:
         pass
