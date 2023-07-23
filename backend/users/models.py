from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN_ROLE = 'admin'
USER_ROLE = 'user'
ROLES = (
    ('user', USER_ROLE),
    ('admin', ADMIN_ROLE),
)


class User(AbstractUser):
    """Custom User model."""
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
        default=USER_ROLE,
        verbose_name='Роль пользователя',
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ADMIN_ROLE
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == ADMIN_ROLE

    check_is_admin = property(is_admin)


class Subscriber(models.Model):
    """Subscriber model."""
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
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'],
                name='unique_subscribe'
            )
        ]
