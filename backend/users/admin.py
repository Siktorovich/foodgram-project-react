from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Subscriber

User = get_user_model()


@register(User)
class CustomUserAdmin(UserAdmin):
    """Class for User model in admin panel."""
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'email',
        'first_name',
    )
    search_fields = (
        'email',
        'first_name',
    )


@register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    """Class for Subscriber model in admin panel."""
    list_display = (
        'user',
        'subscriber',
    )
