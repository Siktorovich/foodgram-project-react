from django.contrib import admin

from recipes.models import Ingridient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'image',
        'is_in_shopping_cart',
        'is_favourited',
    )

admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(Recipe, RecipeAdmin)