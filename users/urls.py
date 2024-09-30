from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegisterView, DashboardView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='users_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView, name='users_dashboard'),
]
