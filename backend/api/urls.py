from django.urls import include, path
from rest_framework import routers

from api.views import (CartView, FavoriteView, IngredientViewSet,
                       RecipeViewSet, SubscribeList, SubscribeView, TagViewSet,
                       download_shopping_cart)

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('users/subscriptions/', SubscribeList.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('recipes/<int:recipe_id>/shopping_cart/', CartView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
