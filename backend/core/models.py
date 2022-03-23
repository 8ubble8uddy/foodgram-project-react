from django.db import models

from api.users.models import User


class CustomModel(models.Model):
    name = models.CharField('Название', max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CustomServiceModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
        verbose_name='Пользователь',
        )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_%(class)s',
                )
            ]
