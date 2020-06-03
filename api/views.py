
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer
# Also add these imports
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsAuthenticatedTrue
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        print('...>>>>', self)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        refresh = RefreshToken.for_user(instance)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'data': serializer.data,
            'message': 'hello',
        })

    def list(self, request, *args, **kwargs):
        # print('>>>><<<<<<.....{}'.format(args[0].headers.get('Authorization')))
        print('>>>><<<<<<.....{}'.format(request.user))
        print('>>>><<<<<<.....{}'.format(request.auth))
        pay = self.get_queryset()
        serializer = self.get_serializer(pay, many=True)
        return Response({
            'data': serializer.data,
            'message': 'hello',
        })

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticatedTrue]
    #     return [permission() for permission in permission_classes]

    # Add this code block
    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer_context = {
    #         'request': request,
    #     }
    #     serializer_context = {
    #         'request': request,
    #     }
    #     serializer = UserSerializer(
    #         queryset, many=True, context=serializer_context)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     serializer_context = {
    #         'request': request,
    #     }
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user, context=serializer_context)
    #     return Response(serializer.data)

    # def create(self, request):


    def get_permissions(self):
        permission_classes = []
        print('...>>>>>{}'.format(self.action))
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
