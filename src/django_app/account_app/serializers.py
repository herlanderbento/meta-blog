from rest_framework import serializers

from src.core.account.domain.user_role import UserRole


class CreateUserInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(
        default=UserRole.USER, choices=[(tag.name, tag.value) for tag in UserRole]
    )
    is_active = serializers.BooleanField(default=False)


class GetUserInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class UpdateUserInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(
        choices=[(tag.name.lower(), tag.value.lower()) for tag in UserRole]
    )
    is_active = serializers.BooleanField(default=False)


class DeleteUserInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
