from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


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
