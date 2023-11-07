from django.contrib import admin

from .models import Category, Recipe, Сookbook


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class СookbookAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "recipe"]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "steps", "cooking_time", "create_at"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Сookbook, СookbookAdmin)
