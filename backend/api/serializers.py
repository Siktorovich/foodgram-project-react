import base64

from django.core.files.base import ContentFile

from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscriber, Tag
from rest_framework import serializers
from users.serializers import UserSerializer

import webcolors


class Hex2NameColor(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('No name for this color')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CartRepresentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe_id.id')
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = (
            'user_id',
            'recipe_id',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        return CartRepresentSerializer(
            instance, context={'request': request}
        ).data


class FavoriteRepresentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe_id.id')
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = (
            'user_id',
            'recipe_id',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        return FavoriteRepresentSerializer(
            instance, context={'request': request}
        ).data


class RecipeSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscriber_id.email')
    id = serializers.ReadOnlyField(source='subscriber_id.id')
    username = serializers.ReadOnlyField(source='subscriber_id.username')
    first_name = serializers.ReadOnlyField(source='subscriber_id.first_name')
    last_name = serializers.ReadOnlyField(source='subscriber_id.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscriber
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

    def get_is_subscribed(self, obj):
        return Subscriber.objects.filter(
            user_id=obj.user_id,
            subscriber_id=obj.subscriber_id
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.subscriber_id)
        return RecipeSubscribeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.subscriber_id).count()


class SubscribeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriber
        fields = (
            'user_id',
            'subscriber_id'
        )

    def validate(self, data):
        if data.get('user_id') == data.get('subscriber_id'):
            raise serializers.ValidationError(
                'You can not subscribe on yourself.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeSerializer(
            instance, context={'request': request}
        ).data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

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
