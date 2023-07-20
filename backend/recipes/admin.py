from django.contrib import admin

from recipes.models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )



class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'favorite_counter',
        'pub_date',
    )
    list_filter = ('author', 'name', 'tags')

    @admin.display(description='Число добавлений в избранное')
    def favorite_counter(self, obj):
        return obj.favorite.count()


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
