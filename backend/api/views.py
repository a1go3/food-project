from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .filters import IngredientFilter, RecipeFilter
from food.models import (Tag, Ingredient, Recipe, IngredientAmount, Favourite,
                         ShoppingCart)
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializers,
                          RecipeInFollowSerializer)
from .pagination import Pagination

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для моделей Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для моделей Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly | IsAdminOrReadOnly]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializers
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favourite, request.user, pk)
        else:
            return self.delete_from(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Вы уже добавили этот рецепт'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeInFollowSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы уже удалили этот рецепт'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        shopping_cart = (
            f'Список покупок для {request.user.username}. \n'
        )
        shopping_cart += '\n'.join([
            f' {num}. {ingredient["ingredient__name"]}'
            f' - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'

            for num, ingredient in enumerate(ingredients, start=1)
        ])

        filename = f'shopping_cart_for_{request.user.username}.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
