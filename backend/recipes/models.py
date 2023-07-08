from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default='user',
        verbose_name='Роль пользователя',
    )
    is_subscribed = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='Подписан ли текущий пользователь на этого'
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


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
        verbose_name='Список ингридиентов',
        related_name='recipe'
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Находится ли в корзине'
    )
    is_favourited = models.BooleanField(
        verbose_name='Находится ли в избранном'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

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

    def __str__(self):
        return f'{self.tag_id} {self.recipe_id}' 


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

    def __str__(self):
        return f'{self.ingredient_id} {self.recipe_id}'


class AmountIngredientInRecipe(models.Model):
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
    amount = models.PositiveBigIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return self.amount


class Subscriber(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    subscriber_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='На кого подписались'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'