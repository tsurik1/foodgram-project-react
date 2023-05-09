from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Описание рецепта."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    tags = models.ManyToManyField(
        to='Tag',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        to='Ingredient',
        related_name='recipes',
        through='RecipeIngredient'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )
    text = models.TextField(
        max_length=150,
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
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Invalid hex code',
                code='invalid_hex'
            ),
        ]
    )
    slug = models.SlugField(unique=True)

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

    def __str__(self):
        return self.name


class Favourite(models.Model):
    """Избранные рецепты."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='избранное',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return self.recipe


class ShoppingCart(models.Model):
    """Рецепты в списке покупок."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_carts',
        verbose_name='рецепт',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='recipeto',
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return self.recipe


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
