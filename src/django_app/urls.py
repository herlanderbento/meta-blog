"""
URL configuration for django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

from src.django_app.authentication_app.views import AuthenticationAPIView


# class CustomSchemaGenerator(OpenAPISchemaGenerator):
#     def get_paths(self, endpoints=None, components=None, request=None, public=None):
#         # A chamada ao super agora armazena a tupla retornada em 'paths' e 'prefix'
#         paths, prefix = super().get_paths(endpoints, components, request, public)

#         # Filtra rotas duplicadas e não existentes
#         filtered_paths = {}
#         for path, methods in paths.items():
#             # Apenas adiciona se não estiver no dicionário
#             if path not in filtered_paths:
#                 filtered_paths[path] = methods

#         return filtered_paths, prefix  # Ret


# class CustomSchemaGenerator(OpenAPISchemaGenerator):
#     def get_paths(self, endpoints=None, components=None, request=None, public=None):
#         # A chamada ao super agora armazena a tupla retornada em 'paths' e 'prefix'
#         paths, prefix = super().get_paths(endpoints, components, request, public)

#         # Filtra rotas para incluir apenas as desejadas
#         filtered_paths = {}
#         allowed_routes = {
#             "api/login": ["post"],  # Login com método POST
#         }

#         for path, methods in paths.items():
#             # Verifica se o caminho está nas rotas permitidas
#             if path in allowed_routes and set(methods).issubset(
#                 set(allowed_routes[path])
#             ):
#                 filtered_paths[path] = methods

#         return filtered_paths, prefix  # Retorna os caminhos filtrados e o prefixo


# class CustomSchemaGenerator(OpenAPISchemaGenerator):
#     def get_paths(self, endpoints=None, components=None, request=None, public=None):
#         paths, prefix = super().get_paths(endpoints, components, request, public)

#         filtered_paths = {}
#         allowed_routes = {
#             "api/login": ["post"], 
#             "api/users": ["post", "get"],
#             "api/users/<uuid:user_id>": ["patch", "get", "delete"], 
#             "api/users/<uuid:user_id>/change-permission": [
#                 "patch"
#             ], 
#         }

#         for path, methods in paths.items():
#             if path in allowed_routes and set(methods).issubset(
#                 set(allowed_routes[path])
#             ):
#                 filtered_paths[path] = methods

#         return filtered_paths, prefix
class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_paths(self, endpoints=None, components=None, request=None, public=None):
        paths, prefix = super().get_paths(endpoints, components, request, public)

        filtered_paths = {}
        allowed_routes = {
            "api/login": ["post"], 
            "api/users": ["post", "get"],
            "api/users/<uuid:user_id>": ["patch", "get", "delete"], 
            "api/users/<uuid:user_id>/change-permission": [
                "patch"
            ], 
        }

        for path, methods in paths.items():
            if path in allowed_routes and set(methods).issubset(set(allowed_routes[path])):
                filtered_paths[path] = methods
            else:
                print(f"Path {path} with methods {methods} is not allowed.")

        return filtered_paths, prefix


schema_view = get_schema_view(
    openapi.Info(
        title="Meta Blog API",
        default_version="v1",
        description="API documentation for the Meta Blog project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@meta-blog.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # generator_class=CustomSchemaGenerator,  # Use sua classe personalizada aqui
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # Rotas para UserAPIView
    path("api/", include("src.django_app.account_app.urls")),
    # Rota para AuthenticationAPIView
    path("api/login", AuthenticationAPIView.as_view(), name="login"),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
