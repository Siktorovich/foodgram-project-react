from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngridientViewSet,
    RecipeViewSet,
    TagViewSet
)


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'ingridients', IngridientViewSet)
router.register(r'tags', TagViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
