from django.contrib.auth.models import AbstractUser

from django.db import models



ROLES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
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
    
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
