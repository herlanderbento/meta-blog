from tracemalloc import BaseFilter
from typing import List, Type
from core.post.domain.post import Post, PostId
from core.post.domain.post_repository import IPostRepository
from core.shared.domain.repositories.search_params import SortDirection
from core.shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)


class PostInMemoryRepository(
    IPostRepository, InMemorySearchableRepository[Post, PostId, BaseFilter]
):
    sortable_fields: List[str] = ["title", "created_at"]

    def find_by_title(self, title: str) -> Post | None:
        return next((post for post in self.items if post.title == title), None)

    def _apply_filter(
        self, items: List[Post], filter_param: str | None = None
    ) -> List[Post]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower(), items)
            return list(filter_obj)

        return items

    def _apply_sort(
        self,
        items: List[Post],
        sort: str | None = None,
        sort_dir: SortDirection | None = None,
    ) -> List[Post]:
        return (
            super()._apply_sort(items, sort, sort_dir)
            if sort
            else super()._apply_sort(items, "created_at", SortDirection.DESC)
        )

    def get_entity(self) -> Type[Post]:
        return Post
