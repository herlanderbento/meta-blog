from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.post.domain.post import Post


@dataclass(slots=True)
class PostOutput:
    id: UUID
    category_id: UUID
    author_id: UUID
    title: str
    content: str
    image_url: str | None
    is_published: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: Post):
        return cls(
            id=entity.id.value,
            category_id=entity.category_id.value,
            author_id=entity.author_id.value,
            title=entity.title,
            content=entity.content,
            image_url=entity.image_url,
            is_published=entity.is_published,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
