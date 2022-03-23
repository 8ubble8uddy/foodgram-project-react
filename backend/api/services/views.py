from django.db.models import Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.decorators import action

from api.recipes.models import Recipe
from api.services.serializers import (RecipeInServiceSerializer,
                                      UserInServiceSerializer)
from api.users.models import User
from core.pagination import CustomPagination
from core.views import CustomServiceViewset


class FavoriteAndShoppingCartViewSet(CustomServiceViewset):
    queryset = Recipe.objects.all()
    serializer_class = RecipeInServiceSerializer

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        return super().service_create_or_destroy(
            service_name='favorite',
            obj=self.get_recipe(),
            )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        return super().service_create_or_destroy(
            service_name='shopping_cart',
            obj=self.get_recipe(),
            )


class SubscribeViewSet(CustomServiceViewset):
    queryset = User.objects.all()
    serializer_class = UserInServiceSerializer

    def get_author(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk):
        return super().service_create_or_destroy(
            service_name='subscribe',
            obj=self.get_author(),
            )


class SubscriptionList(generics.ListAPIView):
    serializer_class = UserInServiceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.annotate(
            is_subscribed=Count(
                'subscribe',
                filter=Q(subscribe__user_id=user.id),
                )
            ).filter(is_subscribed=1)


class DownloadShoppingCart(views.APIView):

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(
            shopping_cart__user_id=user.id
            ).values_list(
                'ingredients__name',
                'ingredients__measurement_unit',
                ).order_by(
                    'ingredients__name'
                    ).annotate(
                        amount=Sum('ingredients_in_recipe__amount')
                        )

    def get(self, request):
        response = HttpResponse(content_type='text/plain')
        header_info = 'attachment; filename=shopping_cart.txt'
        response['Content-Disposition'] = header_info
        ingredients = self.get_queryset()
        lines = []
        for name, unit, amount in ingredients:
            lines.append(f'{name.capitalize()} ({unit}) - {amount}\n')
        response.writelines(lines)
        return response
