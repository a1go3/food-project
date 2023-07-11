from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from food.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializers


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Recipe."""
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializers
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
