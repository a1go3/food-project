from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

app_name = 'api'
