from django.urls import include, path

from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from api.views import (SubscribeView, SubscriptionView,
                       RecipesViewSet, TagViewSet, IngredientViewSet,
                       ShoppingCartView, FavoriteView,
                       DownloadShoppingCart
                       )

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

djoser_urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    path(
        'set_password/',
        UserViewSet.as_view({'post': 'set_password/'}), name='set_password/'
    )
]
urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/', include(djoser_urlpatterns))
]
