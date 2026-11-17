from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import IsAuthenticatedCustom
from authentication.models import Session
from authentication.serializers import (LoginSerializer, ProfileSerializer,
                                        RegistrationSerializer)
from authentication.sessions import create_session
from authentication.utils import create_jwt
from django.conf import settings

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
        with transaction.atomic():
            user.is_active = False
            user.token_version += 1
            user.save(update_fields=['is_active', 'token_version'])
            Session.objects.filter(user=user).delete()
        response = Response({'detail': 'Аккаунт деактивирован'},
                            status=status.HTTP_200_OK)
        response.delete_cookie(key='session_id')
        return response

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
        token_jwt = create_jwt(user)
        session_id = create_session(user)
        response = Response({'token': token_jwt})
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age= 7* 24 * 60 * 60,
            secure=not settings.DEBUG,
            httponly=True,
            samesite='Lax',
        )
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        user = request.user
        with transaction.atomic():
            user.token_version += 1
            user.save(update_fields=['token_version'])
            session = Session.objects.filter(user=user)
            session.delete()
        response = Response({'detail': 'Вы вышли из системы'},
                            status=status.HTTP_200_OK)
        response.delete_cookie(key='session_id')
        return response
