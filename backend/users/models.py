from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Таблица пользователей"""

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'email',
        'password',
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Фамилия',
    )

    email = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Адрес электронной почты',
    )

    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default='user',
        verbose_name='Роль пользователя',
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    """Таблица подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='На кого подписались'
    )

    class Meta:
        unique_together = ('user', 'subscriber')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'