from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.services.views import (DownloadShoppingCart,
                                FavoriteAndShoppingCartViewSet,
                                SubscribeViewSet,
                                SubscriptionList)

router = DefaultRouter()
router.register('recipes', FavoriteAndShoppingCartViewSet)
router.register('users', SubscribeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
        name='download_shopping_cart',
        ),
    path(
        'users/subscriptions/',
        SubscriptionList.as_view(),
        name='subscriptions',
        ),
]
