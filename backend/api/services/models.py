from django.db import models

from api.recipes.models import Recipe
from api.users.models import User

from core.models import CustomServiceModel


class Favorite(CustomServiceModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное',
        )

    class Meta(CustomServiceModel.Meta):
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'


class ShoppingCart(CustomServiceModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупка',
        )

    class Meta(CustomServiceModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


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
