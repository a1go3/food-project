from django.db.models import F
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from food.models import Tag, Ingredient, Recipe, IngredientAmount

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipieReadSerializers(serializers.ModelSerializer):
    """Сериализатор для SAFE_METHODS к рецептам."""
    author = CustomUserSerializer(read_only=True,
                                  default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount')
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipieWrightSerializers(serializers.ModelSerializer):
    """Сериализатор для добавления и изменения рецептов."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAmountSerializer(
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create_amount_ingredient(self, ingredients, recipe):
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_amount_ingredient(
            recipe=recipe,
            ingredients=ingredients)
        return recipe

