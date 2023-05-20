from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (SubscribeView, SubscriptionView,
                       RecipesViewSet, TagsViewSet, IngredientsViewSet
                       )

router = DefaultRouter()

router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
