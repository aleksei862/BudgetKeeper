from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    #path('ping/', views.ping, name='ping'), # Твой старый маршрут
    path('operations/', views.OperationListCreateView.as_view(), name='operation-list'),
    path('operations/<int:pk>/', views.OperationDetailView.as_view(), name='operation-detail'),
    path('admin-only/', views.AdminOnlyView.as_view(), name='admin-only'),

    # JWT Маршруты
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]