from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from uuid import UUID

from src.core.post.domain.image_media import ImageMedia
from src.core.account.domain.user import User
from src.core.account.domain.user_repository import IUserRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.post.application.use_cases.common.exceptions import (
    PostAlreadyExistsException,
)
from src.core.post.domain.post import Post
from src.core.post.domain.post_repository import IPostRepository
from src.core.shared.application.storage_interface import IStorage
from src.core.shared.application.use_cases import UseCase
from src.core.shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.post.application.use_cases.common.post_output import PostOutput


@dataclass
class CreatePostInput:
    author_id: UUID
    category_id: UUID
    title: str
    content: str
    field: Literal["banner", "thumbnail", "thumbnail_half"]
    is_published: bool = True


@dataclass
class CreatePostOutput(PostOutput):
    pass


class CreatePostUseCase(UseCase):
    def __init__(
        self,
        post_repo: IPostRepository,
        user_repo: IUserRepository,
        category_repo: ICategoryRepository,
        storage: IStorage,
    ):
        self.post_repo = post_repo
        self.user_repo = user_repo
        self.category_repo = category_repo
        self.storage = storage

    def execute(self, input: CreatePostInput) -> CreatePostOutput:
        author = self.user_repo.find_by_id(input.author_id)

        if author is None:
            raise NotFoundException(input.author_id, User)

        category = self.category_repo.find_by_id(input.category_id)

        if category is None:
            raise NotFoundException(input.category_id, Category)

        post_with_same_title = self.post_repo.find_by_title(input.post_title)

        if post_with_same_title:
            raise PostAlreadyExistsException()

        post = Post.create(
            author_id=input.author_id,
            category_id=input.category_id,
            title=input.title,
            content=input.content,
            is_published=input.is_published,
        )

        field_mapping = {
            "banner": post.replace_banner,
            "thumbnail": post.replace_thumbnail,
            "thumbnail_half": post.replace_thumbnail_half,
        }

        replace_method = field_mapping.get(input.field)

        if replace_method is None:
            raise EntityValidationException(f"Invalid field value: {input.field}")

        file_path = Path("images") / str(input.id) / input.file_name

        image_media = ImageMedia(
            name=input.file_name,
            raw_location=str(file_path),
        )
        replace_method(image_media)

        self.storage.store(
            file_path,
            input.content,
            input.content_type,
        )

        if post.notification.has_errors():
            raise EntityValidationException(post.notification.errors)

        self.post_repo.insert(post)

        return self.__to_output(post)

    def __to_output(self, entity: Post) -> CreatePostOutput:
        return CreatePostOutput.from_entity(entity)
