from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Уникальный слаг'
    )


class Ingridient(models.Model):
    pass


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
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)'
    )
    tags = models.ManyToManyField(
        Tag,
        through=TagRecipe,
        verbose_name='Список тегов'
    )
    image = models.ImageField(
        # дописать
        verbose_name='Ссылка на картинку на сайте'

    )
    ingridients = models.ManyToManyField(
        Ingridient,
        through=IngridientRecipe,
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
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class IngridientRecipe(models.Model):
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    ),
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )


class Follow(models.Model):
    pass


class Favourite(models.Model):
    pass


class ShoppingList(models.Model):
    pass