from django.db.models import Count, Q
from rest_framework import exceptions, filters, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.recipes.models import Ingredient, Recipe, Tag
from api.recipes.serializers import (IngredientSerializer,
                                     RecipeSerializer,
                                     TagSerializer)

from core.filters import RecipeFilterSet
from core.pagination import CustomPagination
from core.views import http_methods_except


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    http_method_names = http_methods_except('PUT')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.annotate(
            is_favorited=Count(
                'favorite',
                filter=Q(favorite__user_id=user.id),
                )
            ).annotate(
                is_in_shopping_cart=Count(
                    'shopping_cart',
                    filter=Q(shopping_cart__user_id=user.id),
                    )
                )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!'
                )
        super().perform_update(serializer)

    def perform_destroy(self, recipe):
        if recipe.author != self.request.user:
            raise exceptions.PermissionDenied(
                'Удаление чужого контента запрещено!'
                )
        super().perform_destroy(recipe)
