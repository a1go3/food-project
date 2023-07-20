




def download_shopping_cart(request):
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