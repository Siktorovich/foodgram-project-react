from django.core import validators
from django.db import models

from recipes import consts

from users.models import User


class Tag(models.Model):
    """Таблица тегов"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX',
        validators=[
            validators.RegexValidator(
                regex=consts.REGEX_COLOR_FIELD,
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Таблица ингредиентов"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name=consts.INGREDIENT_CONSTRAINT_NAME
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Таблица рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
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
        verbose_name='Время приготовления (в минутах)',
        validators=[
            validators.MinValueValidator(
                consts.MIN_VALUE_FOR_COOKING_TIME,
                message=consts.COOKING_TIME_ERROR
            )
        ],
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        verbose_name='Список тегов'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Ссылка на картинку на сайте'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipe',
        verbose_name='Список ингредиентов',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name=consts.RECIPE_CONSTRAINT_NAME,
            ),
        )

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    """Таблица принадлежности тегов определенному рецепту"""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipes',
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tag_recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        unique_together = ('tag', 'recipe')
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    """Таблица связи ингрдиента и рецепта и количество ингредиентов"""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            validators.MinValueValidator(
                consts.MIN_VALUE_FOR_AMOUNT,
                message=consts.MIN_VALUE_FOR_AMOUNT
            )
        ]
    )

    class Meta:
        unique_together = ('ingredient', 'recipe')
        verbose_name = 'Количество ингрeдиента в рецепте'
        verbose_name_plural = 'Количество ингрeдиентов в рецептах'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    """Таблица избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Подписавшийся'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Список избранного'


class Cart(models.Model):
    """Таблица корзины"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Выбранный рецепт',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список покупок'
