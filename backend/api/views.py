from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from food.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipieReadSerializers, RecipieWrightSerializers, RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('POST', 'PATCH'):
#             return RecipieWrightSerializers
#         return RecipieReadSerializers
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)