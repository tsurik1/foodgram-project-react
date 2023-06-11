from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )
    password = models.CharField(max_length=150, verbose_name='Пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def clean(self):
        if self.pk is not None:
            old_user = User.objects.get(pk=self.pk)
            if self.password != old_user.password:
                raise ValidationError("Нельзя изменять пароль")


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    subscription = models.ForeignKey(
        User,
        related_name='subscription',
        on_delete=models.CASCADE,
        verbose_name='Подписка'
    )

    class Meta:
        ordering = ('subscriber', 'subscription',)
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def clean(self):
        if self.subscriber == self.subscription:
            raise ValidationError('Нельзя подписаться на самого себя')
