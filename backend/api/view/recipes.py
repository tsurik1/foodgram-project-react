from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin

from recipes.models import Recipe, Favorite
from recipes.models import Recipe
from api.permissions import AuthorOrReadOnly
from api.pagination import MyBasePagination
from api.filters import RecipeFilter
from api.serializer.recipes import RecipeReadSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = MyBasePagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddDeleteView(CreateModelMixin, DestroyModelMixin, GenericAPIView):
    add_model = Recipe
    delete_model = Favorite
    add_serializer = None
    permission_classes = (IsAuthenticated,)

    def add_recipe(self, request, pk):
        recipe = get_object_or_404(self.add_model, pk=pk)
        user = request.user.pk
        data = {'recipe': recipe.pk, 'user': user}
        serializer = self.add_serializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_pecipe(self, request, pk):
        recipe = get_object_or_404(self.add_model, pk=pk)
        user = self.request.user
        obj = get_object_or_404(self.delete_model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
