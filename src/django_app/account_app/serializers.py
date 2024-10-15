from rest_framework import serializers


class CreateUserInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=False)


class GetUserInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class UpdateUserInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=False)


class ChangeUserPermissionInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=False)


class DeleteUserInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
