from rest_framework import exceptions, serializers

from api.fields import Base64ImageField, Hex2NameColor
from api.utils import (create_update_fk_recipe_instance,
                       get_recipes_with_limit, get_validated_ingredients_tags)
from recipes import consts
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Subscriber
from users.serializers import UserSerializer


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    """Serializer representing Recipe instances in subcribes endpoint."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class BaseRepresentSerializer(RecipeSubscribeSerializer):
    """The parent class for representing Recipe instances
    that uses related names.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta(RecipeSubscribeSerializer.Meta):
        fields = RecipeSubscribeSerializer.Meta.fields


class BaseCreateSerializer(serializers.ModelSerializer):
    """The parent class for creating instances that include user field and
    use for representing another serializer.
    """
    represent_serializer = None

    class Meta:
        model = None
        fields = (
            'user',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        recipes_limit = self.context.get('recipes_limit')
        return self.represent_serializer(
            instance, context={
                'request': request,
                'recipes_limit': recipes_limit
            }
        ).data


class CartRepresentSerializer(BaseRepresentSerializer):
    """Cart representing serializer."""
    class Meta(BaseRepresentSerializer.Meta):
        model = Cart


class CartCreateSerializer(BaseCreateSerializer):
    """Cart creating instance serializer."""
    represent_serializer = CartRepresentSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Cart
        fields = BaseCreateSerializer.Meta.fields + ('recipe',)


class FavoriteRepresentSerializer(BaseRepresentSerializer):
    """Favorite representing serializer."""
    class Meta(BaseRepresentSerializer.Meta):
        model = Favorite


class FavoriteCreateSerializer(BaseCreateSerializer):
    """Favorite creating instance serializer."""
    represent_serializer = FavoriteRepresentSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Favorite
        fields = BaseCreateSerializer.Meta.fields + ('recipe',)


class SubscribeSerializer(serializers.ModelSerializer):
    """Subscribe serializer."""
    email = serializers.ReadOnlyField(source='subscriber.email')
    id = serializers.ReadOnlyField(source='subscriber.id')
    username = serializers.ReadOnlyField(source='subscriber.username')
    first_name = serializers.ReadOnlyField(source='subscriber.first_name')
    last_name = serializers.ReadOnlyField(source='subscriber.last_name')
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
            user=obj.user,
            subscriber=obj.subscriber
        ).exists()

    def get_recipes(self, obj):
        queryset = get_recipes_with_limit(self, obj)
        return RecipeSubscribeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        queryset = get_recipes_with_limit(self, obj)
        return queryset.count()


class SubscribeUserSerializer(BaseCreateSerializer):
    """Subscribe creating instance serializer."""
    represent_serializer = SubscribeSerializer

    class Meta(BaseCreateSerializer.Meta):
        model = Subscriber
        fields = BaseCreateSerializer.Meta.fields + ('subscriber',)

    def validate(self, data):
        if data.get('user') == data.get('subscriber'):
            raise serializers.ValidationError(
                consts.SUBSCRIBE_ON_YOURSELF_ERROR
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""
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
    """Ingredient serializer that shows the amount of it in particular
    recipe.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient representing serializer."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeRepresentSerializer(serializers.ModelSerializer):
    """Recipe representing serializer."""
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientWithAmountSerializer(
        many=True,
        source='ingredient_recipes'
    )
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
            user=request.user.pk,
            recipe=obj.pk
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(
            user=request.user.pk,
            recipe=obj.pk
        ).exists()


class IngredientCreateRecipe(serializers.ModelSerializer):
    """Ingredient creating instance serializer in recipe."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class RecipeInitialSerializer(serializers.ModelSerializer):
    """Recipe creating instance serializer."""
    image = Base64ImageField()
    ingredients = IngredientCreateRecipe(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

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

    def create(self, validated_data):
        ingredients, tags = get_validated_ingredients_tags(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        create_update_fk_recipe_instance(
            recipe, self, ingredients, tags, IngredientCreateRecipe
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients, tags = get_validated_ingredients_tags(validated_data)
        recipe = Recipe.objects.get(id=instance.id)
        create_update_fk_recipe_instance(
            recipe, self, ingredients, tags, IngredientCreateRecipe
        )
        return super().update(instance, validated_data)

    def validate_name(self, value):
        if Recipe.objects.filter(name=value).exists():
            raise exceptions.ValidationError(
                consts.UNIQUE_NAME_RECIPE + value
            )
        return value

    def validate_ingredients(self, value):
        if len(value) <= 0:
            raise exceptions.ValidationError(
                consts.EMPTY_LIST_INGREDIENTS
            )
        unique_ids_ingredients = []
        for ingredient in value:
            if IngredientCreateRecipe(
                ingredient
            ).data['id'] in unique_ids_ingredients:
                raise exceptions.ValidationError(
                    consts.DUBLICATED_RECIPE_INGREDIENTS
                )
            unique_ids_ingredients.append(
                IngredientCreateRecipe(ingredient).data['id']
            )
            if int(IngredientCreateRecipe(ingredient).data['amount']) <= 0:
                raise exceptions.ValidationError(
                    consts.MIN_VALUE_FOR_AMOUNT
                )
        return value

    def validate_tags(self, value):
        if len(value) <= 0:
            raise exceptions.ValidationError(
                consts.EMPTY_LIST_TAGS
            )
        unique_ids_tags = []
        for tag in value:
            if tag.id in unique_ids_tags:
                raise exceptions.ValidationError(
                    consts.DUBLICATED_RECIPE_TAGS
                )
            unique_ids_tags.append(tag.id)
        return value

    def validate_cooking_time(self, value):
        if value <= 0:
            raise exceptions.ValidationError(
                consts.MIN_VALUE_FOR_COOKING_TIME
            )
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeRepresentSerializer(
            instance, context={'request': request}
        ).data
