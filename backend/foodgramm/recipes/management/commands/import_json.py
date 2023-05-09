import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных в базу'

    def handle(self, *args, **options):
        with open(
            'recipes/data/ingredients.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        for item in data:
            ingredients = Ingredient()
            ingredients.name = item['name']
            ingredients.measurement_unit = item['measurement_unit']
            ingredients.save()
