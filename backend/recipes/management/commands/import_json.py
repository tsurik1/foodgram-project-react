import json
from random import choice

from django.core.management.base import BaseCommand
from faker import Faker
from recipes.models import Ingredient, Tag
from users.models import User


class Command(BaseCommand):
    help = 'Загрузка данных в базу'

    def handle(self, *args, **options):
        with open(
            'recipes/data/ingredients.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)
        ingredient_list = []
        for item in data:
            ingredient = Ingredient(
                name=item['name'],
                measurement_unit=item['measurement_unit']
            )
            ingredient_list.append(ingredient)

        Ingredient.objects.bulk_create(ingredient_list)

        tags = {'Завтрак': 'breakfast', 'Обед': 'lunch', 'Ужин': 'dinner'}
        for tag, slug in tags.items():
            name = tag
            color = choice(
                ['#FFC107', '#795548', '#2196F3', '#4CAF50', '#9C27B0']
            )
            slug = slug
            Tag.objects.create(
                name=name,
                color=color,
                slug=slug
            )

        fake = Faker()
        for _ in range(7):
            username = fake.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            password = fake.password()

            User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
# from faker import Faker
# from myapp.models import Recipe, Tag, Ingredient, RecipeIngredient
# from django.contrib.auth import get_user_model
# from django.core.files import File
# import random

# class Command(BaseCommand):
#     help = 'Create test records for all models'

#     def handle(self, *args, **options):
#         fake = Faker()

#         # Create test records for Recipe model
#         User = get_user_model()
#         users = User.objects.all()
#         tags = Tag.objects.all()
#         ingredients = Ingredient.objects.all()
#         for i in range(10):
#             recipe = Recipe.objects.create(
#                 name=fake.unique.word(),
#                 cooking_time=random.randint(10, 90),
#                 text=fake.text(max_nb_chars=500),
#                 image=File(open('path/to/image.jpg', 'rb')),
#                 author=random.choice(users),
#             )
#             recipe.tags.add(*random.sample(list(tags), 3))
#             recipe_ingredients = [
#                 RecipeIngredient(
#                     recipe=recipe,
#                     ingredient=ingredient,
#                     amount=random.randint(50, 500),
#                 )
#                 for ingredient in random.sample(list(ingredients), 5)
#             ]
#             RecipeIngredient.objects.bulk_create(recipe_ingredients)

#         self.stdout.write(self.style.SUCCESS('Successfully created test records for Recipe model.'))
