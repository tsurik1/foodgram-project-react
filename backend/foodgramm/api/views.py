from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favourite,
    ShoppingCart,
    RecipeIngredient
)
from rest_framework.decorators import action
from rest_framework import viewsets, views, status
from users.models import CustomUser, Subscription
from .serializers import (
    UsersSerializer,
    RecipesSerializer,
    TagsSerializer,
    IngredientsSerializer,
    FavouriteSerializer,
    ShoppingCartSerializer,
    UserListSerializer,
    SubscriptionSerializer
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

    # @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    # def subscribe(self, request, id):


def download_shopping_cart(request):
    ingredients = Ingredient.objects.filter(reci__in_carts__user=request.user).values(
        'ingredient__name', 'ingredient__measurement_unit'
    )
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'

    for ing in ingredients:
        response.write(f"{ing.name} - {ing.price}\n")

    return response


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def create(self, request, pk):
        recipes = Recipe.objects.get(pk=pk)
        ShoppingCart.objects.create(
            user=request.user, recipe=recipes
        )
        return HttpResponse(status=201)

    def destroy(self, request, pk):
        instance = ShoppingCart.objects.get(
            user=request.user, recipe=pk
        )
        self.perform_destroy(instance)
        return HttpResponse(status=400)

    def perform_destroy(self, instance):
        instance.delete()


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def create(self, request, pk):
        recipes = Recipe.objects.get(pk=pk)
        Favourite.objects.create(
            user=request.user, recepis=recipes
        )
        return HttpResponse(status=201)

    def destroy(self, request, pk):
        instance = Favourite.objects.get(
            user=request.user, recepis=pk
        )
        self.perform_destroy(instance)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
