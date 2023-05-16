from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.models import Subscription, User
from recipes.models import Recipe
from api.pagination import MyBasePagination
from serializer.users import (
    SubscriptionSerializer,
)


class SubscriptionView(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = MyBasePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(subscriber=user.id)


class SubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        subscribtion = get_object_or_404(User, pk=pk)
        subscriber = request.user
        data = {'subscription': subscribtion.id, 'subscriber': subscriber.id}
        serializer = SubscriptionSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        subscription = get_object_or_404(User, pk=pk)
        subscriber = request.user
        subscription = get_object_or_404(
            Subscription, subscription=subscription, subscriber=subscriber
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
