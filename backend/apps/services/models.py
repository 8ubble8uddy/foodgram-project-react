from django.db import models

from apps.core.models import CustomServiceModel
from apps.recipes.models import Recipe
from apps.users.models import User


class Favorite(CustomServiceModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное',
        )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
                )
            ]


class ShoppingCart(CustomServiceModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупка',
        )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
                )
            ]


class Subscribe(CustomServiceModel):
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe',
        verbose_name='Подписка',
        )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribing'],
                name='unique_subscribe',
                ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscribing')),
                name='prevent_self_subscribe',
                ),
            ]
