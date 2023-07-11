from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]