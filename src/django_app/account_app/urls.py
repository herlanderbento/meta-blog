from django.urls import path
from src.django_app.account_app.views import UserAPIView

urlpatterns = [
    path("users", UserAPIView.as_view(), name="user-list-create"),
    path("users/<uuid:user_id>", UserAPIView.as_view(), name="user-detail"),
    path(
        "users/<uuid:user_id>/change-permission",
        UserAPIView.as_view(),
        name="user-change-permission",
    ),
]
