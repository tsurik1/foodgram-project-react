from recipes.models import Recipe, Favorite
from api.serializer.favorite import FavoriteSerializer
from .recipes import AddDeleteView


class FavoriteView(AddDeleteView):
    add_model = Recipe
    delete_model = Favorite
    add_serializer = FavoriteSerializer

    def post(self, request, pk):
        return self.add_recipe(request, pk)

    def delete(self, request, pk):
        return self.delete_pecipe(request, pk)
