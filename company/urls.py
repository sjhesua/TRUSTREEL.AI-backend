from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from . import views

urlpatterns = [
    path('', views.subdomain_view, name='inicio_empresa'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/register/', views.RegisterView.as_view(), name='register-user'),
    path('api/test/', views.protected_view, name='test'),
    path('api/help/', views.view_all_routes, name='all-routes'),
    path('api/get-user-id/', views.get_user_id_from_token, name='get-user-id'),
]