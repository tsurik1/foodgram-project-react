from django.db import transaction

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Recipe, Tag, Favorite, ShoppingCart, RecipeIngredient, Ingredient,
)
from .ingredients import IngredientAmountSerializer
from .users import UserListSerializer
from .tags import TagSerializer


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
    tags = TagSerializer(many=True)
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

    def in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        # if self.model.objects.filter(recipe=recipe, user=user).exists():
        #     raise ValidationError('Рецепт уже добавлен')
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.in_list(obj, ShoppingCart)


class RecipeSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
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

    def create_update(self, ingredients, recipe):
        for ingredient_data in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount']
            )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_update(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        instance.tags.clear()
        self.create_update(ingredients, instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('id', 'name', 'image', 'cooking_time',)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.recipe.image:
            url = obj.recipe.image.url
            return request.build_absolute_uri(url)
        return None
