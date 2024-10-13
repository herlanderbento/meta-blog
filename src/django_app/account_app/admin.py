from django.contrib import admin

from src.django_app.account_app.models import UserModel

class UserAdmin(admin.ModelAdmin):
  pass

admin.site.register(UserModel, UserAdmin)