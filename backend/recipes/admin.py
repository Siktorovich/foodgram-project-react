from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag, User


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'image',
        'is_in_shopping_cart',
        'is_favorited',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'password',
    )


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(User, UserAdmin)