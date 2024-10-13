from dataclasses import dataclass
from typing import Any, Generic, List, TypeVar

from src.core.shared.domain.repositories.search_result import SearchResult


PaginationOutputItem = TypeVar("PaginationOutputItem")


@dataclass(slots=True)
class PaginationOutput(Generic[PaginationOutputItem]):
    items: List[PaginationOutputItem]
    total: int
    current_page: int
    per_page: int
    last_page: int

    @classmethod
    def from_search_result(
        cls,
        items: List[PaginationOutputItem],
        result: SearchResult[Any],
    ):
        last_page = max(1, (result.total + result.per_page - 1) // result.per_page)

        return cls(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=last_page,
        )
