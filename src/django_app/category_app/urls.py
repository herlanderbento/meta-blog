from django.urls import path

from src.django_app.category_app.views import CategoryAPIView


urlpatterns = [
    path("categories", CategoryAPIView.as_view(), name="category-list-create"),
    path(
        "categories/<uuid:category_id>",
        CategoryAPIView.as_view(),
        name="category-detail",
    ),
]
