from django.urls import path, include

urlpatterns = [
    path('api/', include('authentication.urls')),
    path('api/', include('access.urls')),
]
