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
    def setUp(self):
        self.user = User.objects.create(username='db_user')
        self.client.force_authenticate(user=self.user)
        tag = Tag.objects.create(
            name='завтрак',
            color='синий',
            slug='breakfast'
        )
        ingredient = Ingredient.objects.create(
            name='яйцо',
            measurement_unit='шт'
        )
        # self.client = APIClient()
        recipe = Recipe.objects.create(
            author=self.user,
            name='Яичница',
            text='Разбей яйца. Пожарь',
            cooking_time='2'
        )
        recipe.tags.add(tag)
        new_recipe = IngredientAmount(
            recipe=recipe,
            ingredient=ingredient,
            amount=10
            )
        new_recipe.save()

    def test_get(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url)
        print(response.data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(Recipe.objects.count(), 1)

    def test_create(self):
        url = reverse('api:recipes-list')
        data = {
            'tags': [
                1
            ],
            'ingredients': [
                {
                    'id': 1,
                    'amount': 3
                }
            ],
            'name': 'Яичница-2',
            'text': 'Разбей яйца и пожарь.',
            'cooking_time': 100
        }
        response = self.client.post(url, data)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(Recipe.objects.count(), 2)
        self.assertEquals(Recipe.objects.get(pk=2).name, 'Яичница-2')

        url_two = reverse('api:recipes-detail', args='1')
        response_two = self.client.get(url_two)
        print(response_two.data)
        self.assertEquals(status.HTTP_200_OK, response_two.status_code)