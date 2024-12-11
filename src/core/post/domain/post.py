from dataclasses import dataclass, field
import datetime
from typing import Annotated

from pydantic import Strict
from src.core.post.domain.image_media import ImageMedia
from src.core.shared.domain.entity import AggregateRoot
from src.core.category.domain.category import CategoryId
from src.core.account.domain.user import UserId
from src.core.shared.domain.value_objects import Uuid


@dataclass
class PostCreateCommand:
    author_id: UserId
    category_id: CategoryId
    title: str
    content: str
    is_published: bool = True


class PostId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class Post(AggregateRoot):
    id: PostId = field(default_factory=PostId)
    author_id: UserId
    category_id: CategoryId
    title: str
    content: str

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    is_published: bool = True

    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(props: PostCreateCommand) -> "Post":
        return Post(
            author_id=props.author_id,
            category_id=props.category_id,
            title=props.title,
            content=props.content,
            is_published=props.is_published,
        )

    @property
    def entity_id(self):
        return self.id.value

    def change_title(self, title: str):
        self.title = title
        self.touch()
        self.validate()

    def change_content(self, content: str):
        self.content = content
        self.touch()
        self.validate()

    def replace_banner(self, banner: ImageMedia):
        self.banner = banner
        self.touch()
        self.validate()

    def replace_thumbnail(self, thumbnail: ImageMedia):
        self.thumbnail = thumbnail
        self.touch()
        self.validate()

    def replace_thumbnail_half(self, thumbnail_half: ImageMedia):
        self.thumbnail_half = thumbnail_half
        self.touch()
        self.validate()

    def published(self):
        self.is_published = True
        self.touch()

    def unpublished(self):
        self.is_published = False
        self.touch()

    def touch(self):
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "author_id": self.author_id,
                "category_id": self.category_id,
                "title": self.title,
                "content": self.content,
                "image_url": self.image_url,
                "is_published": self.is_published,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }
        )
