from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import exceptions, filters, permissions, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as djoser

from api.filters import RecipeFilterSet, UserFilterSet
from api.pagination import CustomPagination
from api.permissions import RecipePermission, UserPermission
from api.serializers import (CustomUserSerializer,
                             IngredientSerializer,
                             RecipeInServiceSerializer,
                             RecipeSerializer,
                             TagSerializer,
                             UserInServiceSerializer)
from apps.core.views import CreateDestroyServiceMixin, http_methods_except
from apps.recipes.models import Ingredient, Recipe, Tag
from apps.users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet, CreateDestroyServiceMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (RecipePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    pagination_class = CustomPagination
    http_method_names = http_methods_except('PUT')

    def get_queryset(self):
        user = self.request.user
        if self.action == 'download_shopping_cart':
            return Recipe.objects.filter(shopping_cart__user=user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeInServiceSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_ingredients(self, recipes):
        if not recipes:
            raise exceptions.ParseError('Список покупок пуст!')
        return Ingredient.objects.filter(
            recipes__in=recipes
            ).values_list(
                'name', 'measurement_unit',
                ).annotate(
                    amount=Sum('ingredient_in_recipes__amount')
                    )

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=cart.txt'
        ingredients = self.get_ingredients(self.get_queryset())
        lines = []
        for name, measurement_unit, amount in ingredients:
            lines.append(f'{name} ({measurement_unit}) - {amount}\n')
        response.writelines(lines)
        return response

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        return super().service_create_or_destroy()

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        return super().service_create_or_destroy()


class CustomUserViewSet(djoser.UserViewSet, CreateDestroyServiceMixin):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (UserPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilterSet
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if self.action == 'subscriptions':
            return User.objects.filter(subscribe__user=user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['subscribe', 'subscriptions']:
            return UserInServiceSerializer
        return super().get_serializer_class()

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        return super().list(request)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        return super().service_create_or_destroy()
