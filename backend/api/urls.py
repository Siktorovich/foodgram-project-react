from django.urls import include, path
from rest_framework import routers

from api.views import (
    FavoriteView,
    IngredientViewSet,
    RecipeViewSet,
    SubscribeList,
    SubscribeView,
    TagViewSet
)


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('users/subscriptions/', SubscribeList.as_view({'get':'list'})),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('', include(router.urls)),
]
