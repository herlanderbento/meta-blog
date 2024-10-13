from src.core.account.domain.user import User, UserId
from src.django_app.account_app.models import UserModel


class UserModelMapper:
    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.entity_id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_entity(model: User) -> User:
        return User(
            id=UserId(model.id),
            name=model.name,
            email=model.email,
            password=model.password,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
