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

    def calculate_ingredients(self, ingredients_data):
        result = {}
        for ingredient_data in ingredients_data:
            ingredient, amount = ingredient_data.values()
            if ingredient.id in result:
                result[ingredient.id] += amount
            else:
                result[ingredient.id] = amount
        return result

    def add_ingredients(self, recipe, ingredients_data):
        total_ingredients = self.calculate_ingredients(ingredients_data)
        for id, amount in total_ingredients.items():
            recipe.ingredients.add(id, through_defaults={'amount': amount})

    def update(self, recipe, validated_data):
        if 'ingredients_in_recipe' in validated_data:
            ingredients_data = validated_data.pop('ingredients_in_recipe')
            recipe.ingredients.clear()
            self.add_ingredients(recipe, ingredients_data)
        return super().update(recipe, validated_data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_in_recipe')
        recipe = super().create(validated_data)
        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)
