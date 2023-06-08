from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscription, User
from api.pagination import MyBasePagination
from api.serializer.users import SubscriptionSerializer


class SubscriptionView(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = MyBasePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(subscriber=user)


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
        users = get_object_or_404(
            Subscription, subscriber=subscriber, subscription=subscription
        )
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
