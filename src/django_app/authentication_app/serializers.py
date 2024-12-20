from rest_framework import serializers


class AuthenticateUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
