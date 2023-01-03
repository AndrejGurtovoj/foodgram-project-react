from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .permissions import IsAuthOrCreateList
from .serializers import (SubscribeSerializer, UserCreateSerializer,
                          UserSerializer)


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """ViewSet с методами GET (list, retrieve) и POST."""
    pass


class UserViewSet(CreateRetrieveListViewSet):
    """
    Создание и получение пользователей
    Методы: GET (list, retrieve), POST.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthOrCreateList]

    serializer_classes = {
        'create': UserCreateSerializer,
        'me': UserSerializer,
        'set_password': SetPasswordSerializer,
        'subscriptions': SubscribeSerializer
    }

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return self.serializer_class

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        """Метод получения профиля текущего пользователя."""
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        """Метод изменения пароля текущего пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password')
        )
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request, *args, **kwargs):
        """Метод получения подписок текущего пользователя."""
        subscribe_users = User.objects.filter(subscribing__user=request.user)
        serializer = self.get_serializer(subscribe_users, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class SubscriptionView(views.APIView):
    """
    Подписки (подписаться/отписаться)
    Методы: POST, DELETE
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        subscribe_user = get_object_or_404(User, id=user_id)
        double_subscribe = Subscription.objects.filter(
            user=request.user,
            subscribe=subscribe_user
        ).exists()
        if request.user.id == int(user_id):
            error = {'errors': 'Невозможно подписаться на самого себя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        elif double_subscribe:
            error = {'errors': 'Вы уже подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(
            user=request.user,
            subscribe=subscribe_user
        )
        serializer = SubscribeSerializer(
            subscribe_user,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscribe_user = get_object_or_404(User, id=user_id)
        try:
            subscribe = Subscription.objects.get(
                user=request.user,
                subscribe=subscribe_user
            )
        except ObjectDoesNotExist:
            error = {'errors': 'Вы не подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
