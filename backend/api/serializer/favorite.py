from rest_framework import serializers

from recipes.models import Favorite
from api.serializer.recipes import ShortRecipeSerializer


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', 'user',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = ShortRecipeSerializer(
            instance,
            context=context
        )
        return serializer.data
