from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientsViewSet,
    RecipesViewSet,
    TagsViewSet,
    UsersViewSet
)

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
