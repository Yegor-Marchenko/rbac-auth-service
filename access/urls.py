from django.urls import path

from access.views import (AccessRuleDetailView, AccessRuleListView,
                          OrderDetailView, OrderListView, ReviewDetailView,
                          ReviewListView)

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('rules/', AccessRuleListView.as_view(), name='rules-list'),
    path('rules/<int:pk>/', AccessRuleDetailView.as_view(), name='rules-detail'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:id>/', ReviewDetailView.as_view(), name='review-detail'),
]
