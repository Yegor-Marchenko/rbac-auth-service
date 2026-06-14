from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import IsAuthenticatedCustom
from authentication.serializers import (LoginSerializer, ProfileSerializer,
                                        RegistrationSerializer)
from authentication.utils import create_jwt


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user,
                                       data=request.data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.token_version += 1
        user.save(update_fields=['is_active', 'token_version'])
        return Response({'detail': 'Аккаунт деактивирован'},
                        status=status.HTTP_200_OK)


class RegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = create_jwt(user)
        return Response({'token': token})


class LogoutView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        user = request.user
        user.token_version += 1
        user.save(update_fields=['token_version'])
        return Response({'detail': 'Вы вышли из системы'},
                        status=status.HTTP_200_OK)
