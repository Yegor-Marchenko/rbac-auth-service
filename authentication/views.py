from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from authentication.permissions import IsAuthenticatedCustom, IsAdminRole
from authentication.models import Session, AccessRule
from authentication.serializers import (LoginSerializer, ProfileSerializer,
                                        RegistrationSerializer,
                                        AccessRuleSerializer)
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



class AccessRuleListView(ListCreateAPIView):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminRole]


class AccessRuleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminRole]


class MockObject:
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner


FAKE_ORDERS = [
    MockObject(id=1, owner=2),
    MockObject(id=2, owner=99),
]


class OrderListView(APIView):
    resource_name = 'order'

    def get(self, request):
        rule = AccessRule.objects.filter(
            role=request.user.role,
            resource__title=self.resource_name,
        ).first()

        if request.user.is_admin or (rule and rule.read_all_permission):
            orders = FAKE_ORDERS
        else:
            orders = [o for o in FAKE_ORDERS if o.owner == request.user.id]

        data = [{'id': o.id, 'owner': o.owner} for o in orders]
        return Response(data)


class OrderDetailView(APIView):
    resource_name = 'order'

    def get(self, request, id):
        order = None
        for o in FAKE_ORDERS:
            if o.id == id:
                order = o
                break

        if order is None:
            raise NotFound('заказа не найден')

        self.check_object_permissions(request, order)

        return Response({'id': order.id, 'owner': order.owner})


FAKE_REVIEWS = [
    MockObject(id=1, owner=2),
    MockObject(id=2, owner=99),
]


class ReviewListView(APIView):
    resource_name = 'review'

    def get(self, request):
        rule = AccessRule.objects.filter(
            role=request.user.role,
            resource__title=self.resource_name,
        ).first()

        if request.user.is_admin or (rule and rule.read_all_permission):
            reviews = FAKE_REVIEWS
        else:
            reviews = [r for r in FAKE_REVIEWS if r.owner == request.user.id]

        data = [{'id': r.id, 'owner': r.owner} for r in reviews]
        return Response(data)


class ReviewDetailView(APIView):
    resource_name = 'review'

    def get(self, request, id):
        review = None
        for r in FAKE_REVIEWS:
            if r.id == id:
                review = r
                break

        if review is None:
            raise NotFound('Отзыв не найден')

        self.check_object_permissions(request, review)

        return Response({'id': review.id, 'owner': review.owner})
