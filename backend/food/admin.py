from django.contrib import admin
from django.contrib.admin import display

from .models import (Favourite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class MembershipInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipiesAdmin(admin.ModelAdmin):
    list_display = ('author', 'image', 'name', 'text', 'cooking_time')
    list_filter = ('name', 'author', 'tags')
    inlines = [
        MembershipInline
    ]
    exclude = ('ingredients',)

    @display(description='Количество добавлений рецепта в избранное')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
