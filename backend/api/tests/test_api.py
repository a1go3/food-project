import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from food.models import Tag, Ingredient, Recipies
from api.serializers import RecipiesSerializers


class FoodApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_username')


    def test_create(self):
        url = reverse('recipes-list')
        data = {
                "tag": [
                    {
                        "id": 1,
                        "name": "завтрак",
                        "color": "серый",
                        "slug": "breakfast"
                    }
                ],
                "author": {
                    "email": "zljaka@yandex.ru",
                    "id": 1,
                    "username": "roman",
                    "first_name": "",
                    "last_name": ""
                },
                "ingredient": [
                    {
                        "id": 1,
                        "name": "Соль",
                        "measurement_unit": "грамм"
                    }
                ],
                "name": "Яичница",
                "image": "http://127.0.0.1:8000/food/images/1200px-Three_fried_eggs.jpg",
                "text": "Разбей яйца. Пожарь",
                "cooking_time": 10
            }