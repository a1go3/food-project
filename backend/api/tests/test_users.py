from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from food.models import Tag, Ingredient, Recipe, IngredientAmount

User = get_user_model()


# class UsersApiTestCase(APITestCase):
#     def setUp(self):
        # self.user = User.objects.create(username='test_user')
        # self.client.force_authenticate(user=self.user)
        # self.user_two = User.objects.create(username='test_user_two')
        # self.client.force_authenticate(user=self.user_two)
        # tag = Tag.objects.create(
        #     name='завтрак',
        #     color='синий',
        #     slug='breakfast'
        # )
        # tag_two = Tag.objects.create(
        #     name='обед',
        #     color='красный',
        #     slug='lunch'
        # )
        # tag_two.save()
        #
        # ingredient = Ingredient.objects.create(
        #     name='яйцо',
        #     measurement_unit='шт'
        # )
        # ingredient_two = Ingredient.objects.create(
        #     name='молоко',
        #     measurement_unit='л'
        # )
        # ingredient_two.save()
        #
        # recipe = Recipe.objects.create(
        #     author=self.user,
        #     name='Яичница',
        #     text='Разбей яйца. Пожарь',
        #     cooking_time='2'
        # )
        # recipe.tags.add(tag)
        # new_recipe = IngredientAmount(
        #     recipe=recipe,
        #     ingredient=ingredient,
        #     amount=10
        # )
        # new_recipe.save()


class UsersTests(APITestCase):
    def test_create_account(self):
        url = reverse('users:user-list')
        data = {
            'email': '15@mail.ru',
            'username': 'Test3',
            'first_name': 'Test3',
            'last_name': 'Test3',
            'password': 'zaq123wsx'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, 'Test3')

    def test_subscribe(self):
        self.user = User.objects.create(username='test_user')
        self.user_two = User.objects.create(username='test_user_two')
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user_two)
        url = reverse('users:user-subscribe', args=1)
