from django_filters import rest_framework as filters

from rest_framework import viewsets

from recipes.models import Ingredient
from api.permissions import ReadOnly
from api.filters import IngredientFilter
from api.serializer.ingredients import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    permission_classes = (ReadOnly,)
