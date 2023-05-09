from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favourite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from users.models import CustomUser, Subscription

from .filters import RecipeFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (
    IngredientsSerializer,
    RecipeReadSerializer,
    RecipesSerializer,
    ShortRecipeSerializer,
    SubscriptionSerializer,
    TagsSerializer
)

User = get_user_model()


class UsersViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(subscriber=request.user)
        queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        subscribtion = CustomUser.objects.get(pk=id)
        subscriber = request.user
        if request.method == 'POST':
            if subscribtion == subscriber:
                return Response({
                    'errors': 'Вы не можете подписываться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(
                subscriber=subscriber, subscription=subscribtion
            ).exists():
                return Response({
                    'errors': 'Вы уже подписаны'
                }, status=status.HTTP_400_BAD_REQUEST)
            subscribtions = Subscription.objects.create(
                subscriber=subscriber, subscription=subscribtion
            )
            serializer = SubscriptionSerializer(
                subscribtions, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if subscribtion == subscriber:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not Subscription.objects.filter(
            subscriber=subscriber, subscription=subscribtion
        ).exists():
            return Response({
                'errors': 'Вы не были подписаны'
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = Subscription.objects.get(
            subscriber=request.user, subscription=id
        )
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name']
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = ('tags',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = Recipe.objects.get(pk=pk)
            user = request.user
            if Favourite.objects.filter(recipe=recipe, user=user).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в список избранных'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = ShortRecipeSerializer(recipe)
            Favourite.objects.create(recipe=recipe, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(pk=pk)
        instance = Favourite.objects.get(
            recipe=recipe.id, user=request.user
        )
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = Recipe.objects.get(pk=pk)
            user = request.user
            if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в список покупок'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = ShortRecipeSerializer(recipe)
            ShoppingCart.objects.create(recipe=recipe, user=user)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        recipe = Recipe.objects.get(pk=pk)
        recipe_in_cart = ShoppingCart.objects.get(
            recipe=recipe.id, user=request.user
        )
        recipe_in_cart.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = []
        ingredients = Ingredient.objects.filter(
            recipeingredient__recipe__in_carts__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('recipeingredient__amount'))

        for ing in ingredients:
            shopping_list.append(
                f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
