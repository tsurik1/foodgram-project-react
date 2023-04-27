from django.urls import path, include
from .views import (
    UsersViewSet,
    RecipesViewSet,
    TagsViewSet,
    IngredientsViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('users', UsersViewSet)
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
