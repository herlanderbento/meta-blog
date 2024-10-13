from uuid import uuid4
from django.db import models

from src.django_app.account_app.models import UserModel


class UserTokenModel(models.Model):
    app_label = "authentication_app"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    refresh_token = models.CharField(max_length=255)
    expires_date = models.DateField(auto_now_add=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_tokens"
    )
    created_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        db_table = "user_tokens"
        ordering = ["-created_at"]
