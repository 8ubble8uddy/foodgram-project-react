from django.contrib import admin

from apps.recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count')
    list_filter = ('author', 'name', 'tags')

    def favorite_count(self, obj):
        return obj.favorite.count()

    favorite_count.short_description = 'Число добавлений в избранное'


admin.site.register(IngredientInRecipe)
admin.site.register(Tag)
