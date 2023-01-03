from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientsFilter(filters.FilterSet):
    """Фильтр ингредиентов по названию."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelMultipleChoiceFilter(
        field_name='author__id',
        to_field_name='id',
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_favorited_shop_cart')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_favorited_shop_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def _get_params(self, key):
        return {f'{key}__user': self.request.user}

    def filter_favorited_shop_cart(self, queryset, name, value):
        params = {
            'is_favorited': self._get_params('favorites'),
            'is_in_shopping_cart': self._get_params('shopping_cart')
        }
        if value:
            return queryset.filter(**params[name])
        return queryset.exclude(**params[name])
