from rest_framework import serializers
from djoser import serializers as djoser
from drf_base64.serializers import Base64ImageField

from api.fields import ServiceSerializerField
from apps.core.serializers import CustomServiceSerializer
from apps.recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from apps.users.models import User

USER_FIELDS = ('email', 'id', 'username', 'first_name', 'last_name')


class CustomUserSerializer(djoser.UserSerializer):
    is_subscribed = ServiceSerializerField(service='subscribe')

    class Meta:
        model = User
        fields = USER_FIELDS + ('is_subscribed',)


class CustomUserCreateSerializer(djoser.UserCreateSerializer):

    class Meta:
        model = User
        fields = USER_FIELDS + ('password',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
        )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
        )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
        )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredients_in_recipe',
        many=True,
        )
    is_favorited = ServiceSerializerField(service='favorite')
    is_in_shopping_cart = ServiceSerializerField(service='shopping_cart')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            )

    def validate_ingredients(self, value):
        ingredients = []
        for data in value:
            if data['ingredient'] in ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты в рецепте не должны повторяться!'
                    )
            ingredients.append(data['ingredient'])
        return value

    def add_ingredients(self, recipe, ingredients):
        for data in ingredients:
            recipe.ingredients.add(
                data['ingredient'],
                through_defaults={'amount': data['amount']},
                )

    def update(self, recipe, validated_data):
        if 'ingredients_in_recipe' in validated_data:
            ingredients = validated_data.pop('ingredients_in_recipe')
            recipe.ingredients.clear()
            self.add_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in_recipe')
        recipe = super().create(validated_data)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)


class RecipeInServiceSerializer(CustomServiceSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


class UserInServiceSerializer(CustomServiceSerializer):
    is_subscribed = ServiceSerializerField(service='subscribe')
    recipes = RecipeInServiceSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = USER_FIELDS + ('is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()

    def validate(self, data):
        if self.context['request'].user == self.instance:
            raise serializers.ValidationError(
                'Пользователь не может подписаться сам на себя!'
                )
        return super().validate(data)
