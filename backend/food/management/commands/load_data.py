import csv

from django.core.management import BaseCommand
from food.models import Ingredient

PATH = '../data/'
INGREDIENTS = 'ingredients.csv'
MESSAGE = 'был успешно загружен в базу данных.'
UTF = 'UTF-8'


class Command(BaseCommand):
    help = 'Загружает данные из csv файлов в базу данных'

    def handle(self, *args, **options):
        with open(
                f'{PATH}{INGREDIENTS}',
                'r',
                encoding=UTF
        ) as csvFile:
            data = csv.reader(csvFile, delimiter=',')
            Ingredient.objects.bulk_create(
                Ingredient(
                    name=name,
                    measurement_unit=measurement_unit) for
                name, measurement_unit in data)
            self.stdout.write(self.style.SUCCESS(
                f'{INGREDIENTS} {MESSAGE}'))
