from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Subscriber

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Class for Subscriber model in admin panel."""
    list_display = (
        'user',
        'subscriber',
    )
