import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from food.models import Tag, Ingredient, Recipe, IngredientAmount
from api.serializers import RecipieWrightSerializers, RecipieReadSerializers


class FoodApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='db_user')

    def test_create(self):
        url = reverse('recipes-list')
        data = {
            "tags": [
                1,
                2
            ],

            "ingredients": [
                {
                    "id": 1,
                    "amount": 2
                }
            ],
            "name": "Яичница-2",

            "text": "Разбей яйца и Пожарь еще",
            "cooking_time": 10
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)