import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД'

    def handle(self, *args, **options):
        with open(
                './data/ingredients.json',
                encoding='utf-8'
        ) as data:
            for row in json.load(data):
                ingredient = Ingredient(
                    name=row['name'].capitalize(),
                    measurement_unit=row['measurement_unit']
                )
                ingredient.save()
