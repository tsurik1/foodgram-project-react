from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Recipe, Tag, Favorite, ShoppingCart, RecipeIngredient, Ingredient,
)
from ingredients import IngredientAmountSerializer
from users import UserListSerializer


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserListSerializer()
    ingredients = IngredientAmountSerializer(
        source='recipeingredient_set',
        read_only=True, many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipesSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserListSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data
