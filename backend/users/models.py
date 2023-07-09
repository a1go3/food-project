from django.contrib.auth.models import AbstractUser
from django.db import models


# class User(AbstractUser):
#     """Модель пользователя. """
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [
#         'username',
#         'first_name',
#         'last_name',
#     ]
#     email = models.EmailField(
#         'email address',
#         max_length=254,
#         unique=True,
#     )
#
#     class Meta:
#         ordering = ['id']
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return self.username

class User(AbstractUser):
    """Модель пользователя. """
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=25,
        unique=True,
        help_text='Введите адрес электронной почты',
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=15,
        unique=True,
        help_text='Придумайте никнейм',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=15,
        help_text='Введите имя',
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=15,
        help_text='Введите фамилию',
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        help_text='Введите пароль',
    )


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~models.Q(user=models.F('following')),
                                   name='not_self_follow')

        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'