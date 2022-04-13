from django.db.models import OuterRef, Prefetch, Subquery
from django_filters import rest_framework as filters

from apps.recipes.models import Recipe, Tag
from apps.users.models import User


class RecipeFilterSet(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
        )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags')

    def filter_is_favorited(self, *args):
        return self.filter_service(*args, service='favorite')

    def filter_is_in_shopping_cart(self, *args):
        return self.filter_service(*args, service='shopping_cart')

    def filter_service(self, queryset, name, value, service):
        user = self.request.user
        kwargs = {'{}__{}'.format(service, 'user_id'): user.id}
        return queryset.filter(**kwargs) if value else queryset


class UserFilterSet(filters.FilterSet):
    recipes_limit = filters.NumberFilter(method='filter_recipes_limit')

    class Meta:
        model = User
        fields = ('recipes_limit',)

    def filter_recipes_limit(self, queryset, name, limit):
        return queryset.prefetch_related(
            Prefetch(
                'recipes', queryset=Recipe.objects.filter(
                    id__in=Subquery(
                        Recipe.objects.filter(
                            author_id=OuterRef('author_id')
                            ).values_list('id', flat=True)[:limit]
                        )
                    )
                )
            ) if 'subscriptions' in self.request.path else queryset
