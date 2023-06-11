from rest_framework import serializers

from recipes.models import ShoppingCart
from api.serializer.recipes import ShortRecipeSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('recipe', 'user',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = ShortRecipeSerializer(
            instance,
            context=context
        )
        return serializer.data
