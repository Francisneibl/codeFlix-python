from django.contrib import admin

from djangoproject.category_app.models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
