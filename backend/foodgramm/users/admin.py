from django.contrib import admin

from .models import CustomUser, Subscription


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')
    search_fields = ('email', 'username')


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subscriber', 'subscription')
