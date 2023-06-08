from django.db.models import Sum
from django.http import HttpResponse

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, ShoppingCart, RecipeIngredient
from api.serializer.cart import ShoppingCartSerializer
from .recipes import AddDeleteView


class ShoppingCartView(AddDeleteView):
    add_model = Recipe
    delete_model = ShoppingCart
    add_serializer = ShoppingCartSerializer

    def post(self, request, pk):
        return self.add_recipe(request, pk)

    def delete(self, request, pk):
        return self.delete_pecipe(request, pk)


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
