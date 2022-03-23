from rest_framework import serializers
from drf_base64.serializers import Base64ImageField

from api.recipes.models import Recipe
from api.users.models import User
from core.serializers import CustomServiceSerializer


class RecipeInServiceSerializer(CustomServiceSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')

    def validate(self, data):
        return super().service_validate(data)


class UserInServiceSerializer(CustomServiceSerializer):
    is_subscribed = serializers.BooleanField(read_only=True, default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes(self, author):
        recipes = author.recipes.all()
        query_params = self.context['request'].query_params
        if query_params.get('recipes_limit'):
            recipes_limit = query_params.get('recipes_limit')
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                pass
        return RecipeInServiceSerializer(recipes, many=True).data

    def validate(self, data):
        if self.context['request'].user == self.instance:
            raise serializers.ValidationError(
                'Пользователь не может подписаться сам на себя!'
                )
        return super().service_validate(data)
