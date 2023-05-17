from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')
    search_fields = ('email', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk',)
