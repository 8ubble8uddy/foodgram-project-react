from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from api.users.models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            )

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            user != author and
            author.subscribe.filter(user_id=user.id).exists()
            )


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            )
