from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.conf import settings

from users.models import User


class Recipe(models.Model):
    """Описание рецепта."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    tags = models.ManyToManyField(
        to='Tag',
        related_name='recipes',
        verbose_name='Тег'
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name='Ингредиент'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                settings.LIMIT_VALUE,
                f'минимальное время приготовления '
                f'{settings.LIMIT_VALUE} минута'
            ),
        )
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='img_recipe',
        blank=True,
        verbose_name='Загрузить фото'
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        verbose_name='время добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тег для блюда."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Invalid hex code',
                code='invalid_hex'
            ),
        ]
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиенты для блюда."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Скачивание списка ингредиентов для покупки."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингридент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество'
    )

    class Meta:
        verbose_name = "ингредиент в рецепте"
        verbose_name_plural = "ингредиенты в рецепте"
