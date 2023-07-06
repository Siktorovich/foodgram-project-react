from django.contrib.auth import get_user_model

from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        )

class IngredientWithAmountSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(source='amount_ingredient.amount')
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientWithAmountSerializer(many=True)
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favourited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )