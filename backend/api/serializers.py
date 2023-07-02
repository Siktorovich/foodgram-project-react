from rest_framework import serializers

from recipes.models import Ingridient, Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingridients',
            'is_favourited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all_'


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = '__all__'