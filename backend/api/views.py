from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters

from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError

from users.models import Subscription, User
from recipes.models import (
    Ingredient, Recipe, Tag, ShoppingCart, Favorite, RecipeIngredient
)
from .permissions import AuthorOrReadOnly
from .pagination import MyBasePagination
from .filters import IngredientFilter, RecipeFilter
from .serializer.ingredients import IngredientSerializer
from .serializer.tags import TagSerializer
from .serializer.users import SubscriptionSerializer, ShortRecipeSerializer
from .serializer.recipes import RecipeReadSerializer, RecipeSerializer


class SubscriptionView(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = MyBasePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(subscriber=user.id)


class SubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        subscribtion = get_object_or_404(User, pk=pk)
        subscriber = request.user
        data = {'subscription': subscribtion.id, 'subscriber': subscriber.id}
        serializer = SubscriptionSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        subscription = get_object_or_404(User, pk=pk)
        subscriber = request.user
        subscription = get_object_or_404(
            Subscription, subscription=subscription, subscriber=subscriber
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class AddDelView(APIView):

    permission_classes = (IsAuthenticated,)

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def del_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(AddDelView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        return self.add_recipe(ShoppingCart, request, pk)

    def delete(self, request, pk):
        return self.del_recipe(ShoppingCart, request, pk)


class FavoriteView(AddDelView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        return self.add_recipe(Favorite, request, pk)

    def delete(self, request, pk):
        return self.del_recipe(Favorite, request, pk)


class DownloadShoppingCart(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = []
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_carts__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        for ing in ingredients:
            shopping_list.append(
                f"{ing['ingredient__name']}: "
                f"{ing['amount']} {ing['ingredient__measurement_unit']}"
            )
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
