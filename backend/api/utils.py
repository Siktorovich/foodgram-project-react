import io

from django.http import FileResponse
from reportlab.lib.pagesizes import inch, letter
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe


def creating_pdf_list(ingredients):
    """Creating pdf file function."""
    buffer = io.BytesIO()
    pdfmetrics.registerFont(ttfonts.TTFont(
        'Garamond', 'static/Garamond.ttf'
    ))
    my_canvas = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    text = my_canvas.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont(
        psfontname='Garamond',
        size=16
    )

    for index, ingredient in enumerate(ingredients):
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']
        line = f'{index+1}. {name.title()} ({measurement_unit}) - {amount}'

    text.textLine(line)
    my_canvas.drawText(text)
    my_canvas.showPage()
    my_canvas.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='your_shop_list.pdf',
        content_type='application/pdf',
    )


class QuerySerializer(serializers.Serializer):
    """Serializer for query param."""
    query = serializers.IntegerField(min_value=0)


def query_validation(query_param):
    """Validation function for qury param recipes_limit."""
    query_serializer = QuerySerializer(data={'query': query_param})
    query_serializer.is_valid(raise_exception=True)


def get_recipes_with_limit(serializer_instance, subscriber_instance):
    """Util that get from context query param recipes_limit and if it
    was transfer return limit queryset of recipes.
    """
    recipes_limit = serializer_instance.context.get('recipes_limit')
    if recipes_limit is not None:
        return subscriber_instance.subscriber.recipes.all()[
            :int(recipes_limit)
        ], True
    return subscriber_instance.subscriber.recipes.all(), False


def is_patch_method(action_instance):
    """Function that proving that HTTP method is PATCH."""
    return action_instance.context['request'].method == 'PATCH'


def create_update_fk_recipe_instance(
    recipe,
    action_instance,
    ingredients,
    tags,
    encoded_serializer
):
    """Util that create links with recipes if it was transfer."""
    if ingredients:
        if is_patch_method(action_instance):
            recipe.ingredient_recipes.all().delete()
        ingredient_list = [
            IngredientRecipe(
                recipe=recipe,
                ingredient=Ingredient.objects.get(
                    id=encoded_serializer(ingredient).data['id'],
                ),
                amount=encoded_serializer(ingredient).data['amount']
            ) for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredient_list)
    if tags:
        if is_patch_method(action_instance):
            recipe.tags.clear()
        recipe.tags.set(tags)


def get_validated_ingredients_tags(validated_data):
    """Util that pop values from validated data.
    Default value is False if key does not exist.
    """
    ingredients = validated_data.pop('ingredients', False)
    tags = validated_data.pop('tags', False)
    return ingredients, tags
