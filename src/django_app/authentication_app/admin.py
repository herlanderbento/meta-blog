from django.contrib import admin

from src.django_app.authentication_app.models import UserTokenModel


class UserTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserTokenModel, UserTokenAdmin)
