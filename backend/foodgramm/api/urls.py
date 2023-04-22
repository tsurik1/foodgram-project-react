from django.urls import path, include
from .views import (
    UsersViewSet,
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet,
    FavouriteViewSet,
    ShoppingCartViewSet,
    download_shopping_cart
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('users', UsersViewSet)
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('recipes/<int:pk>/favorite/', FavouriteViewSet.as_view(
        {'post': 'create',
         'delete': 'destroy'}
    )),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view(
        {'post': 'create',
         'delete': 'destroy'}
    )),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    
]
