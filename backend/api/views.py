from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework import response, decorators, views, viewsets, status, mixins, generics
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag, Subscriber, User
from api.serializers import (
    CartCreateSerializer,
    FavoriteCreateSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    SubscribeSerializer,
    SubscribeUserSerializer,
)
from api.utils import CreateDeleteAPIView


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscribeView(views.APIView):
    def post(self, request, user_id):
        serializer = SubscribeUserSerializer(
            data={'user_id':request.user.id, 'subscriber_id':user_id}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        subscribe = get_object_or_404(
            Subscriber,
            user_id=request.user.id,
            subscriber_id=user_id
        )
        subscribe.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeList(ListViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(user_id=self.request.user)


class FavoriteView(views.APIView):
    
    def post(self, request, recipe_id):
        serializer = FavoriteCreateSerializer(
            data={'user_id': request.user.id, 'recipe_id': recipe_id}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        favorite = get_object_or_404(
            Favorite,
            user_id=request.user.id,
            recipe_id=recipe_id
        )
        favorite.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CartView(views.APIView):
   
    def post(self, request, recipe_id):
        serializer = CartCreateSerializer(
            data={'user_id': request.user.id, 'recipe_id': recipe_id}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        cart = get_object_or_404(
            Cart,
            user_id=request.user.id,
            recipe_id=recipe_id
        )
        cart.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
