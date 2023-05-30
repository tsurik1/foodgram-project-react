from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer
)
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from users.models import Subscription, User


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',  'first_name', 'last_name', 'password'
        )


class UserListSerializer(DjoserUserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request')
        if user is None or user.user.is_anonymous:
            return False
        author = Subscription.objects.filter(
            subscriber=user.user, subscription=obj.pk)
        if obj.pk == user.user.pk:
            return False
        return author.exists()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscription')
        validators = [UniqueTogetherValidator(
            queryset=Subscription.objects.all(),
            fields=['subscriber', 'subscription'],
            message='Вы уже подписаны'
        )]

    def validate(self, data):
        subscriber = data.get('subscriber')
        subscription = data.get('subscription')
        if subscriber == subscription:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscribeSerializer(
            instance,
            context=context
        )
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscription.email')
    id = serializers.ReadOnlyField(source='subscription.id')
    username = serializers.ReadOnlyField(source='subscription.username')
    first_name = serializers.ReadOnlyField(source='subscription.first_name')
    last_name = serializers.ReadOnlyField(source='subscription.last_name')
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.subscription)
        serializer = ShortRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.subscription.recipes.count()
