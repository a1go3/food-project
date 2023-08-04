from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.serializers import RecipeInFollowSerializer
from food.models import IngredientAmount, Recipe


def downloading(request):
    """Функция для скачивания файла со списком покупок. """
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

def add_delete_recipe(request, pk, models):
    """Функция для добавления и удаления рецепта из избранного
    или списка покупок. """
    if request.method == 'POST':
        if models.objects.filter(user=request.user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Вы уже добавили этот рецепт'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        models.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeInFollowSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        obj = models.objects.filter(user=request.user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы уже удалили этот рецепт'},
            status=status.HTTP_400_BAD_REQUEST
        )
