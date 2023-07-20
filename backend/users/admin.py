from django.contrib import admin

from users.models import User, Subscriber


class UserAdmin(admin.ModelAdmin):
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
        'name',
    )


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscriber',
    )


admin.register(User, UserAdmin)
admin.register(Subscriber, SubscriberAdmin)