from src.core.account.domain.user_token import UserToken
from src.core.account.domain.user_token_repository import IUserTokenRepository
from src.django_app.account_app.models import UserModel
from src.django_app.authentication_app.mappers import UserTokenModelMapper


class UserTokenDjangoRepository(IUserTokenRepository):

    def insert(self, entity: UserToken) -> None:
        model, relations = UserTokenModelMapper.to_model(entity)

        user = UserModel.objects.get(id=relations.user_id)

        model.user = user

        model.save()

    def find_by_refresh_token(self, refresh_token: str) -> UserToken | None:
        model = UserModel.objects.filter(refresh_token=refresh_token).first()
        return UserTokenModelMapper.to_entity(model) if model else None

    def delete(self, entity_id: str) -> None:
        UserModel.objects.filter(id=entity_id).delete()
