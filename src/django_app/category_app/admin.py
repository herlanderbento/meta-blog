from django.contrib import admin

from src.django_app.category_app.models import CategoryModel

class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(CategoryModel, CategoryAdmin)
