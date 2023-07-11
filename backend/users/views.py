from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, views, viewsets
from recipes.models import User

from users.serializers import UserCreateSerializer, UserSerializer

class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class UserMeView(views.APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        print(request.user.pk)
        user = get_object_or_404(queryset, pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)