from django.contrib import admin

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag, TagRecipe)


class TagAdmin(admin.ModelAdmin):
    """Class for Tag model in admin panel."""
    list_display = ('name', 'color', 'slug',)


class IngredientAdmin(admin.ModelAdmin):
    """Class for Ingredient model in admin panel."""
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class IngredientInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 1


class TagInline(admin.StackedInline):
    model = TagRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """Class for Recipe model in admin panel."""
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'get_tags',
        'get_ingredients',
        'favorite_counter',
        'pub_date',
    )
    list_filter = ('author', 'name', 'tags',)
    search_fields = ('author', 'name', 'tags',)
    inlines = [IngredientInline, TagInline]

    @admin.display(description='tags')
    def get_tags(self, obj):
        return [*(tag.name for tag in obj.tags.all())]

    @admin.display(description='ingredients')
    def get_ingredients(self, obj):
        return '\n '.join([
            f"{ingredient['ingredient__name']} "
            f"({ingredient['ingredient__measurement_unit']}) - "
            f"{ingredient['amount']}"
            for ingredient in obj.ingredient_recipes.values(
                'ingredient__name', 'ingredient__measurement_unit',
                'amount'
            )])

    @admin.display(description='Counter of adding in favorite')
    def favorite_counter(self, obj):
        return obj.favorite.count()


class IngredientRecipeAdmin(admin.ModelAdmin):
    """Class for UngredientRecipe model in admin panel."""
    list_display = ('recipe', 'ingredient', 'amount',)


class CartAdmin(admin.ModelAdmin):
    """Class for Cart model in admin panel."""
    list_display = ('user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    """Class for Favorite model in admin panel."""
    list_display = ('user', 'recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
