from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
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

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser,
        related_name='subscriber',
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        CustomUser,
        related_name='subscription',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('subscriber', 'subscription')
