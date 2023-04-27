from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favourite,
    ShoppingCart,
)
from rest_framework.decorators import action
from rest_framework import viewsets, status
from users.models import CustomUser, Subscription
from .serializers import (
    RecipesSerializer,
    TagsSerializer,
    IngredientsSerializer,
    UserListSerializer,
    SubscriptionSerializer,
    ShortRecipeSerializer
)
from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
User = get_user_model()


class UsersViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, id=None):
        author = get_object_or_404(User, id=id)
        serializer = UserListSerializer(
            author, context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserListSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(subscriber=request.user)
        queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscribe(self, request, id):
        if request.method == 'POST':
            subscribtion = CustomUser.objects.get(pk=id)
            subscriber = request.user
            subscribtions = Subscription.objects.create(
                subscriber=subscriber, subscription=subscribtion
            )
            serializer = SubscriptionSerializer(
                subscribtions, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        instance = Subscription.objects.get(
            subscriber=request.user, subscription=id
        )
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = Recipe.objects.get(pk=pk)
            user = request.user
            serializer = ShortRecipeSerializer(recipe)
            Favourite.objects.create(recipe=recipe, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(pk=pk)
        instance = Favourite.objects.get(
            recipe=recipe.id, user=request.user
        )
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = Recipe.objects.get(pk=pk)
            user = request.user
            serializer = ShortRecipeSerializer(recipe)
            ShoppingCart.objects.create(recipe=recipe, user=user)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        recipe = Recipe.objects.get(pk=pk)
        instance = ShoppingCart.objects.get(
            recipe=recipe.id, user=request.user
        )
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = self.request.user

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = []
        ingredients = Ingredient.objects.filter(
            recipeingredient__recipe__in_carts__user=user
        ).values(
            'name',
            measurement=F('measurement_unit')
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
