import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from food.models import Tag, Ingredient, Recipe, IngredientAmount


class FoodApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='db_user')
        Tag.objects.create(
            name='завтрак',
            color='синий',
            slug='breakfast'
        )
        Ingredient.objects.create(
            name='яйцо',
            measurement_unit='шт'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_create(self):
        url = reverse('api:recipes-list')
        data = {
            'tags': [
                1
            ],
            'ingredients': [
                {
                    'id': 1,
                    'amount': 2
                }
            ],
            'name': 'Яичница',
            'text': 'Разбей яйца и пожарь.',
            'cooking_time': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(Recipe.objects.count(), 1)
        self.assertEquals(Recipe.objects.get().name, 'Яичница')
