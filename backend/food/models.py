from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='Название тега'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор')


    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=20,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения')

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        related_name='recipes',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент',
        through='IngredientAmount'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='food/images/',
        null=True,
        default=None
    )
    name = models.CharField(
        max_length=16,
        verbose_name='Название')
    text = models.CharField(
        max_length=200,
        verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки',
        default=0
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~models.Q(user=models.F('following')),
                                   name='not_self_follow')

        ]


class IngredientAmount(models.Model):
    """Модель, отвечающая за количество ингредиентов в рецепте. """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
    )

    def __str__(self):
        return f'{self.amount} {self.ingredient}'
