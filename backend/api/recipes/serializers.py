from rest_framework import serializers
from drf_base64.serializers import Base64ImageField

from api.recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from api.users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
        )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
        )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='ingredients_in_recipe',
        )
    is_favorited = serializers.BooleanField(
        read_only=True,
        default=False,
        )
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True,
        default=False,
        )
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

    def update(self, recipe, validated_data):
        if 'ingredients_in_recipe' in validated_data:
            ingredients_data = validated_data.pop('ingredients_in_recipe')
            recipe.ingredients.clear()
            for ingredient in ingredients_data:
                recipe.ingredients.add(
                    ingredient['ingredient'],
                    through_defaults={'amount': ingredient['amount']},
                    )
        return super().update(recipe, validated_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_in_recipe')
        recipe = super().create(validated_data)
        for ingredient in ingredients_data:
            recipe.ingredients.add(
                ingredient['ingredient'],
                through_defaults={'amount': ingredient['amount']},
                )
        return recipe

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)
