from django.contrib import admin

from .models import CustomUser, Subscription


class UsersAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'username')


class SubscriptionsAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'subscriber', 'subscription')


admin.site.register(CustomUser, UsersAdmin)
admin.site.register(Subscription, SubscriptionsAdmin)
