from rest_framework import serializers
from users.serializers import UserSerializer
from recipes.models import Cart, Favorite, Recipe, Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientWithAmountSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(source='amount_ingredient.amount')

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
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
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

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
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Cart.objects.filter(
            user_id=request.user.pk,
            recipe_id=obj.pk
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(
            user_id=request.user.pk,
            recipe_id=obj.pk
        ).exists()