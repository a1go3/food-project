from csv import DictReader

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from food.models import Ingredient

PATH = '../data/'
INGREDIENTS = 'ingredients.csv'
MESSAGE = 'был успешно загружен в базу данных.'
UTF = 'UTF-8'


class Command(BaseCommand):
    help = 'Загружает данные из csv файлов в базу данных'

    def load_ingredients(self):
        for row in DictReader(
                open(f'{PATH}{INGREDIENTS}', encoding=UTF)):
            Ingredient.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'{INGREDIENTS} {MESSAGE}')
        )

    def handle(self, *args, **options):
        try:
            self.load_ingredients()

        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(
                f'ERROR - {err}')
            )
            exit()