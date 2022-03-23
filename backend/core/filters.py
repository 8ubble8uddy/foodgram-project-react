from django_filters.rest_framework import BooleanFilter, CharFilter, FilterSet

from api.recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')
    tags = CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')
