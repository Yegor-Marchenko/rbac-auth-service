from django.urls import path

from authentication.views import (LoginView, LogoutView, ProfileView,
                                  RegistrationView, OrderListView,
                                  OrderDetailView, AccessRuleListView,
                                  AccessRuleDetailView, ReviewListView,
                                  ReviewDetailView)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),

    path('rules/', AccessRuleListView.as_view(), name='rules-list'),
    path('rules/<int:pk>/', AccessRuleDetailView.as_view(), name='rules-detail'),

    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:id>/', ReviewDetailView.as_view(), name='review-detail'),
]
