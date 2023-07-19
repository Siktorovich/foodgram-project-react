import base64

from api.mixins import (
    RepresentSerializerMixin
)
from api.fields import Base64ImageField, Hex2NameColor
from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Subscriber,
    Tag,
    TagRecipe
)
from rest_framework import serializers
from users.serializers import UserSerializer


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class BaseRepresentSerializer(RecipeSubscribeSerializer):
    id = serializers.ReadOnlyField(source='recipe_id.id')
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')

    class Meta(RecipeSubscribeSerializer.Meta):
        fields = RecipeSubscribeSerializer.Meta.fields


class BaseCreateSerializer(serializers.ModelSerializer):
    represent_serializer = None

    class Meta:
        model = None
        fields = (
            'user_id',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        return self.represent_serializer(
            instance, context={'request': request}
        ).data


class CartRepresentSerializer(BaseRepresentSerializer):
    class Meta(BaseRepresentSerializer.Meta):
        model = Cart


class CartCreateSerializer(BaseCreateSerializer):
    represent_serializer = CartRepresentSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Cart
        fields = BaseCreateSerializer.Meta.fields + ('recipe_id',)


class FavoriteRepresentSerializer(BaseRepresentSerializer):

    class Meta(RepresentSerializerMixin.Meta):
        model = Favorite


class FavoriteCreateSerializer(BaseCreateSerializer):
    represent_serializer = FavoriteRepresentSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Favorite
        fields = BaseCreateSerializer.Meta.fields + ('recipe_id',)


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


class SubscribeUserSerializer(BaseCreateSerializer):
    represent_serializer = SubscribeSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Subscriber
        fields = BaseCreateSerializer.Meta.fields + ('subscriber_id',)

    def validate(self, data):
        if data.get('user_id') == data.get('subscriber_id'):
            raise serializers.ValidationError(
                'You can not subscribe on yourself.'
            )
        return data


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
    name = serializers.StringRelatedField()
    measurement_unit = serializers.StringRelatedField()
    amount = serializers.ReadOnlyField(source='ingredient_recipe.amount')

    class Meta:
        model = IngredientRecipe
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


class RecipeRepresentSerializer(serializers.ModelSerializer):
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


class RecipeInitialSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    # def create(self, validated_data):
    #     ingredients = self.initial_data.pop('ingredients')
    #     tags = self.initial_data.pop('tags')
    #     recipe = Recipe.objects.create(**validated_data)

    #     for ingredient in ingredients:
    #         current_ingredient = Ingredient.objects.get(
    #             id=ingredient['id']
    #         )
    #         if int(ingredient['amount']) < 1:
    #             raise serializers.ValidationError(
    #                 'Amount can be less than 1'
    #             )
    #         AmountIngredientInRecipe.objects.create(
    #             ingredient_id=current_ingredient,
    #             recipe_id=recipe,
    #             amount=ingredient['amount']
    #         )
    #         IngredientRecipe.objects.create(
    #             ingredient_id=current_ingredient, recipe_id=recipe
    #         )
    #     for tag in tags:
    #         current_tag, status = Tag.objects.get_or_create(
    #             **tag
    #         )
    #         TagRecipe.objects.create(
    #             tag_id=current_tag, recipe_id=recipe
    #         )
    #     return recipe
    
    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     return RecipeRepresentSerializer(
    #         instance, context={'request': request}
    #     ).data