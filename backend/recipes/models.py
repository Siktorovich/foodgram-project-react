from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        unique = True,
        verbose_name='Уникальный слаг'
    )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )



class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Список тегов'
    )
    image = models.ImageField(
        upload_to = 'recipes/images/',
        verbose_name='Ссылка на картинку на сайте'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Список ингридиентов'
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Находится ли в корзине'
    )
    is_favourited = models.BooleanField(
        verbose_name='Находится ли в избранном'
    )

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag_id = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipe',
        verbose_name='Тег'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tag_recipe',
        verbose_name='Рецепт'
    )


class IngredientRecipe(models.Model):
    ingredient_id = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Ингридиент'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Рецепт'
    )


class AmountIngridientInRecipe(models.Model):
    ingredient_id = ingredient_id = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Ингридиент'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_recipe',
        verbose_name='Рецепт'
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Количество'
    )
