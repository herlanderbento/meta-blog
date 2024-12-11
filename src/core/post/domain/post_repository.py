from abc import ABC
from src.core.post.domain.post import Post, PostId
from src.core.shared.domain.repositories.repository_interface import ISearchableRepository
from src.core.shared.domain.repositories.search_params import SearchParams
from src.core.shared.domain.repositories.search_result import SearchResult


class PostSearchParams(SearchParams[str]):
    pass


class PostSearchResult(SearchResult[Post]):
    pass


class IPostRepository(ISearchableRepository[Post, PostId], ABC):
    def find_by_title(self, title: str) -> Post | None:
        pass
