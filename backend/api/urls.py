from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (SubscribeView, SubscriptionView,
                       RecipesViewSet, TagViewSet, IngredientViewSet,
                       ShoppingCartView, FavoriteView
                       )

router = DefaultRouter()

router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('recipes/download_shopping_cart/', ShoppingCartView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
