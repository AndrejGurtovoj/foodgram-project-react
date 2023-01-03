from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteShoppingCartView, IngredientsViewSet,
                    RecipesViewSet, TagsViewSet)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/<recipe_id>/favorite/',
        FavoriteShoppingCartView.as_view(),
        name='favorite'
    ),
    path(
        'recipes/<recipe_id>/shopping_cart/',
        FavoriteShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path('', include('users.urls')),
    path('', include(router.urls)),
]
