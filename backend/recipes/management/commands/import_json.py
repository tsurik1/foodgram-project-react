from django.core.management.base import BaseCommand
from django.db import models

import json
from random import choice
from faker import Faker

from recipes.models import Ingredient, Tag
from users.models import User, Subscription


class CommandHistory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_executed = models.BooleanField(default=False)


class Command(BaseCommand):
    help = 'Загрузка данных в базу'
    command_name = 'load_data'
    is_executed = CommandHistory.objects.filter(
        name=command_name, is_executed=True
    ).exists()
    if not is_executed:
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

            tags = {'Завтрак': 'breakfast',
                    'Обед': 'lunch', 'Ужин': 'dinner'}
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

            users = User.objects.all()
            for user in users:
                random_users = User.objects.exclude(
                    id=user.id)
                for random_user in random_users:
                    Subscription.objects.create(
                        subscriber=user,
                        subscription=random_user
                    )
