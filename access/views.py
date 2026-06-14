from rest_framework.exceptions import NotFound
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from access.models import AccessRule
from access.permissions import IsAdminRole
from access.serializers import AccessRuleSerializer


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

        if rule and rule.read_all_permission:
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

        if rule and rule.read_all_permission:
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
