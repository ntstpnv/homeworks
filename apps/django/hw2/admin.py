from django.contrib import admin

from . import models


class RecipeInline(admin.TabularInline):
    model = models.Recipe
    extra = 1


@admin.register(models.Dish)
class DishAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    inlines = [RecipeInline]


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
